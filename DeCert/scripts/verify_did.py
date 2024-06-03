import json
from brownie import DIDRegistry, accounts
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature

def verify_did(did_document):
    # 从 DID 文档中提取必要信息
    did = did_document["id"]
    proof = did_document["proof"]
    verification_method_id = proof["verificationMethod"]
    proof_value = proof["proofValue"]
    public_key_pem = None

    # 从区块链上获取 DID 文档
    did_registry = DIDRegistry[-1]
    did_document_on_chain = did_registry.getDIDDocument(did)

    # 查找对应的 verificationMethod
    for vm in did_document_on_chain[5]:  # verificationMethods is the 6th element in the tuple
        if vm[0] == verification_method_id:
            public_key_pem = vm[2]
            break

    if public_key_pem is None:
        return False, "Verification method not found"

    # 加载公钥
    public_key = load_pem_public_key(public_key_pem.encode())

    # 反序列化 DID 文档并移除 proofValue 字段
    did_document_copy = did_document.copy()
    did_document_copy["proof"].pop("proofValue")
    did_document_json = json.dumps(did_document_copy, separators=(',', ':')).encode()

    # 验证签名
    try:
        public_key.verify(
            bytes.fromhex(proof_value),
            did_document_json,
            ec.ECDSA(hashes.SHA256())
        )
        return True, "Verification successful"
    except InvalidSignature:
        return False, "Invalid signature"