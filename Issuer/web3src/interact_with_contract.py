from web3 import Web3
from datetime import datetime, timezone
from .get_signature import Signature
from .tuple_to_json import did_document_to_json
import json
import os
# # 连接到以太坊节点 (这里以本地节点为例)
# w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
#
# # 读取ABI
# b_dir = os.path.dirname(os.path.abspath(__file__))
# c_path = os.path.join(b_dir, 'DIDRegistry_abi.json')
# with open(c_path, 'r') as abi_file:
#     abi = json.load(abi_file)
#
# # 使用提供的地址进行交易
# account = w3.eth.accounts[0]

def generate_did(w3, abi, account, contract_address, context, created, updated, version, publicKeyPems, typesOfKey):
    """在链上生成DID"""
    contract = w3.eth.contract(address=contract_address, abi=abi)
    tx_hash = contract.functions.generateDID(
        context, created, updated, version, publicKeyPems, typesOfKey
    ).transact({'from': account})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    logs = contract.events.DIDCreated().process_receipt(tx_receipt)
    return logs[0]['args']['did']

def get_did_document(w3, abi, contract_address, did):
    """获取链上的DID Document"""
    contract = w3.eth.contract(address=contract_address, abi=abi)
    return contract.functions.getDIDDocument(did).call()

def add_proof(w3, abi, account_address, contract_address, did, typeOfProof, created, proofPurpose, verificationMethod, proofValue):
    """在链上添加证明信息"""
    contract = w3.eth.contract(address=contract_address, abi=abi)
    tx_hash = contract.functions.addProof(
        did, typeOfProof, created, proofPurpose, verificationMethod, proofValue
    ).transact({'from': account_address})
    w3.eth.wait_for_transaction_receipt(tx_hash)

def get_current_time():
    # 获取当前时间，使用 UTC 时区
    now = datetime.now(timezone.utc)
    # 格式化为 ISO 8601 字符串
    iso8601_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    return iso8601_time
def register_did(w3, abi, account_address, contract_address, public_key_pem, type_of_key, add_proof_private_key_pem):
    context = "https://www.w3.org/ns/did/v1"
    created = get_current_time()
    updated = get_current_time()
    version = "1.0"
    did = generate_did(
        w3,
        abi,
        account_address,
        contract_address,
        context,
        created,
        updated,
        version,
        public_key_pem,
        type_of_key,
    )
    print(f"Generated DID: {did}")
    did_document = get_did_document(w3, abi, contract_address, did)
    did_document = did_document_to_json(did_document)
    add_proof_verificationMethod = did_document["verificationMethod"][0]
    type_of_proof = add_proof_verificationMethod["type"]
    proof_created = get_current_time()
    proof_purpose = "assertionMethod"
    verification_method = add_proof_verificationMethod["id"]
    proof_value = Signature(did_document, type_of_proof, add_proof_private_key_pem)

    add_proof(
        w3,
        abi,
        account_address,
        contract_address,
        did,
        type_of_proof,
        proof_created,
        proof_purpose,
        verification_method,
        proof_value
    )
    updated_did_document = get_did_document(w3, abi, contract_address, did)
    updated_did_document = did_document_to_json(updated_did_document)
    return updated_did_document
# if __name__ == "__main__":
#     # 生成DID
#     did = generate_did(
#         contract_address,
#         "https://www.w3.org/ns/did/v1",
#         "2023-06-01T00:00:00Z",
#         "2023-06-01T00:00:00Z",
#         "1.0",
#         ["pem1", "pem2"],
#         ["type1", "type2"]
#     )
#     print(f"Generated DID: {did}")
#
#
#     # 获取DID Document
#     did_document = get_did_document(contract_address, did)
#     print(f"DID Document: {did_document}")
#
#     # 添加证明信息
#     add_proof(
#         contract_address,
#         did,
#         "exampleProof",
#         "2023-06-01T00:00:00Z",
#         "assertionMethod",
#         "did:dc:123#key-0",
#         "proofValue"
#     )
#     updated_did_document = get_did_document(contract_address, did)
#     print(f"Updated DID Document: {updated_did_document}")