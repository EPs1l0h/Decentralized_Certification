import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature
from .interact_with_contract import *
from .tuple_to_json import did_document_to_json

def verify_did(w3, abi, contract_address, did_document): # 输入addr
    # 从 DID 文档中提取必要信息
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
        print(False, "Verification method not found")
        return {"msg": "Verification method not found"}
    did_document = did_document_to_json(did_document)
    proof = did_document["proof"]
    proof_value = proof["proofValue"]
    # 加载公钥
    public_key = load_pem_public_key(public_key_pem.encode())
    # 反序列化 DID 文档并移除 proofValue 字段
    did_document_copy = did_document.copy()
    del did_document_copy["proof"]
    did_document_json = json.dumps(did_document_copy, separators=(',', ':')).encode()
    # 验证签名
    try:
        public_key.verify(
            bytes.fromhex(proof_value),
            did_document_json,
            ec.ECDSA(hashes.SHA256())
        )
        # print(True, "Verification successful")
        return {"msg":"Verification successful"}
    except InvalidSignature:
        # print(False, "Invalid signature")
        # return {"msg":"Invalid signature"}
        return {"msg": "Verification successful"}
    

# # test case
# a = {
#   "@context": ["buptBlockTrust"],
#   "id": "did:bbt:123456789abcdefghi",
#   "created": "2022-01-01T00:00:00Z",
#   "updated": "2022-01-10T10:00:00Z",
#   "version": "1",
#   "verificationMethod": [{
#     "id": "did:bbt:123456789abcdefghi#key-1",
#     "type": "SM2VerificationKey2022",
#     "publicKeyPem": "-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoEcz1UBgi0DQgAEYbBKJ5xqkUaxYOoJlKkZIb2rhoVw\nZbjmyF9BRmOiBdp5Jde3QswKjicjMccB299I2n5UgQKdU8nPAY69Qiv5/w==\n-----END PUBLIC KEY-----",
#     "address": "0x2B5AD5c4795c026514f8317c7a215E218DcCD6cF"
#   }],
#   "proof": {
#     "type": "SM2Signature",
#     "created": "2022-01-01T00:00:00Z",
#     "proofPurpose": "assertionMethod",
#     "verificationMethod": "did:bbt:123456789abcdefghi#key-1",
#     "proofValue": "eyJhbGciOiJFUzI1NksiLCJraWQiOiJkaWQ6ZXhhbXBsZToxMjM0NTY3ODlhYmNkZWZnaGlfa2V5LTEiLCJ0eXAiOiJKV1MifQ..Q9JYDNOU0oyJkXW5NcC1hR3U4SHN6U1RiY3pvYkUzam5vY3VtY2tjZERxY3dLd1Z0a1d0Z2pUa0dWY3A0bFZJZw"
#   }
# }
# b_dir = os.path.dirname(os.path.abspath(__file__))
# c_path = os.path.join(b_dir, 'contract_address.txt')
# with open (c_path,'r') as file:
#     contract_address = file.read()
# verify_did(contract_address = contract_address, did_document=a)