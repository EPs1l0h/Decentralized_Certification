from brownie import DIDRegistry
from get_account import getAccount
from datetime import datetime, timezone
from get_signature import Signature

def get_current_time():
    # 获取当前时间，使用 UTC 时区
    now = datetime.now(timezone.utc)
    # 格式化为 ISO 8601 字符串
    iso8601_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    return iso8601_time


def register_did(account_name, context, version, public_key_pem, type_of_key, add_proof_private_key_pem):
    # 使用第一个账户进行部署和交互
    account = getAccount(account_name)
    # 部署合约
    did_registry = DIDRegistry.deploy({'from': account})
    created = get_current_time()
    updated = get_current_time()
    did = did_registry.generateDID(
        context, created, updated, version, public_key_pem, type_of_key, {'from': account}
    )

    print(f"DID generated: {did}")

    # 获取DID Document
    did_document = did_registry.getDIDDocument(did)
    print(f"DID Document: {did_document}")
    add_proof_verificationMethod = did_document["verificationMethod"][0]
    # 添加Proof
    type_of_proof = add_proof_verificationMethod["type"]
    proof_created = get_current_time()
    proof_purpose = "assertionMethod"
    verification_method = add_proof_verificationMethod["id"]
    proof_value = Signature(did_document, type_of_proof, add_proof_private_key_pem)

    did_registry.addProof(
        did, type_of_proof, proof_created, proof_purpose, verification_method, proof_value, {'from': account}
    )

    # 获取更新后的DID Document
    updated_did_document = did_registry.getDIDDocument(did)
    print(f"Updated DID Document: {updated_did_document}")
