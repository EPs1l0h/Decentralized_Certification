from web3 import Web3
import json
import os
from web3.exceptions import ContractLogicError  # 导入 ContractLogicError 异常

# 连接到以太坊节点 (这里以本地节点为例)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# 读取ABI
b_dir = os.path.dirname(os.path.abspath(__file__))
c_path = os.path.join(b_dir, 'DIDRegistry_abi.json')
with open(c_path, 'r') as abi_file:
    abi = json.load(abi_file)

# 使用提供的地址进行交易
account = '0x23F884761b3779a6fa8016660772f3aA638908AF'

# 从文件中读取合约地址
b_dir = os.path.dirname(os.path.abspath(__file__))
c_path = os.path.join(b_dir, 'contract_address.txt')
with open(c_path, 'r') as f:
    contract_address = f.read().strip()

def generate_did(contract_address, context, created, updated, version, publicKeyPems, typesOfKey):
    """在链上生成DID"""
    contract = w3.eth.contract(address=contract_address, abi=abi)
    tx_hash = contract.functions.generateDID(
        context, created, updated, version, publicKeyPems, typesOfKey
    ).transact({'from': account})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    logs = contract.events.DIDCreated().process_receipt(tx_receipt)
    return logs[0]['args']['did']

def get_did_document(contract_address, did):
    """获取链上的DID Document"""
    contract = w3.eth.contract(address=contract_address, abi=abi)
    return contract.functions.getDIDDocument(did).call()

def add_proof(contract_address, did, typeOfProof, created, proofPurpose, verificationMethod, proofValue):
    """在链上添加证明信息"""
    contract = w3.eth.contract(address=contract_address, abi=abi)
    tx_hash = contract.functions.addProof(
        did, typeOfProof, created, proofPurpose, verificationMethod, proofValue
    ).transact({'from': account})
    w3.eth.wait_for_transaction_receipt(tx_hash)

if __name__ == "__main__":
    try:
        # 生成DID
        did = generate_did(
            contract_address,
            "https://www.w3.org/ns/did/v1",
            "2023-06-01T00:00:00Z",
            "2023-06-01T00:00:00Z",
            "1.0",
            ["pem1", "pem2"],
            ["type1", "type2"]
        )
        print(f"Generated DID: {did}")
    except ContractLogicError as e:
        if "DID already exists for this address" in str(e):
            print("DID already exists for this address.")
            # 假设我们知道 DID，可以设置一个已知的 DID 进行测试
            did = "did:dc:23f884761b3779a6fa8016660772f3aa638908af"
        else:
            raise

    # 获取DID Document
    did_document = get_did_document(contract_address, did)
    print(f"DID Document: {did_document}")

    # 添加证明信息
    add_proof(
        contract_address,
        did, 
        "exampleProof", 
        "2023-06-01T00:00:00Z", 
        "assertionMethod", 
        "did:dc:123#key-0", 
        "proofValue"
    )
    updated_did_document = get_did_document(contract_address, did)
    print(f"Updated DID Document: {updated_did_document}")
