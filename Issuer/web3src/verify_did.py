import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature
from .interact_with_contract import *
from .tuple_to_json import did_document_to_json

def verify_did(w3, abi, contract_address, did_document): # 输入addr
    # 从 DID 文档中提取必要信息
    print("============================================================")
    print(did_document)
    did = did_document["id"]
    proof = did_document["proof"]
    verification_method_id = proof["verificationMethod"]
    proof_value = proof["proofValue"]
    public_key_pem = None
    did_document = get_did_document(w3, abi, contract_address, did)
    # 从区块链上获取 DID 文档
    did_document_on_chain = did_document

    # 查找对应的 verificationMethod
    for vm in did_document_on_chain[5]:  # verificationMethods is the 6th element in the tuple
        if vm[0] == verification_method_id:
            public_key_pem = vm[2]
            break

    if public_key_pem is None:
        return False
    did_document = did_document_to_json(did_document)
    proof = did_document["proof"]
    proof_value = proof["proofValue"]
    # 加载公钥
    public_key = load_pem_public_key(public_key_pem.encode())
    # 反序列化 DID 文档并移除 proofValue 字段
    did_document_copy = did_document.copy()
    del did_document_copy["proof"]
    did_document_json = json.dumps(did_document_copy).encode()
    # 验证签名
    try:
        public_key.verify(
            bytes.fromhex(proof_value),
            did_document_json,
            ec.ECDSA(hashes.SHA256())
        )
        # print(True, "Verification successful")
        return True
    except InvalidSignature:
        # print(False, "Invalid signature")
        return False
        # return {"msg": "Verification successful"}
    
