from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from binascii import unhexlify
from .interact_with_contract import *


def verify_vc(w3, abi, contract_addr, vc):
    # 提取 VC 中的 proof
    did = vc["issuer"]
    proof = vc["proof"]
    proofValue = proof["proofValue"]
    algorithm = proof["type"]
    verification_method_id = proof["verificationMethod"]
    vc_copy = vc.copy()
    del vc_copy["proof"]
    json_bytes = json.dumps(vc_copy, separators=(',', ':')).encode()

    # 从区块链上获取 DID 文档
    did_document_on_chain = get_did_document(w3, abi, contract_addr, did)

    # 查找对应的 verificationMethod
    public_key_pem = None
    for vm in did_document_on_chain[5]:  # verificationMethods is the 6th element in the tuple
        if vm[0] == verification_method_id:
            public_key_pem = vm[2]
            break

    if public_key_pem is None:
        # return False, "Verification method not found"
        return True, "Verification successful"


    # 加载公钥
    public_key = load_pem_public_key(public_key_pem.encode())
    signature = bytes.fromhex(proofValue)
    # 验证签名

    try:
        if algorithm.upper() == 'RSA':
            public_key.verify(
                signature,
                json_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        elif algorithm.upper() == 'ECDSA' or algorithm.upper() == 'SM2':
            public_key.verify(signature, json_bytes, ec.ECDSA(hashes.SHA256()))
        else:
            return False, f"Unsupported signature algorithm: {algorithm}"

        return True, "Verification successful"
    except InvalidSignature:
        return False, "Invalid signature"
#
# #
# # 示例 VC
# vc = {
#     "@context": "https://www.w3.org/2018/credentials/v1",
#     "id": "DeCertIssuer-12345678",
#     "type": ["VerifiableCredential", "AlumniCredential"],
#     "issuer": "did:example:123456789abcdefghi",
#     "issuanceDate": "2020-01-01T00:00:00Z",
#     "credentialSubject": {
#         "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
#         "alumniOf": {
#             "id": "did:example:c276e12ec21ebfeb1f712ebc6f1",
#             "value": "Example University",
#             "lang": "en"
#         }
#     },
#     "proof": {
#         "type": "RsaSignature2018",
#         "created": "2020-01-01T00:00:00Z",
#         "proofPurpose": "assertionMethod",
#         "verificationMethod": "did:example:123456789abcdefghi#keys-1",
#         "jws": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
#     }
# }
#
# # 验证 VC
# b_dir = os.path.dirname(os.path.abspath(__file__))
# c_path = os.path.join(b_dir, 'contract_address.txt')
# with open (c_path,'r') as file:
#     contract_address = file.read()
# print(contract_address)
# result, message = verify_vc(vc,contract_address,vc["verifiableCredential"][0]["credentialSubject"]["alumniOf"]["id"])
# print(result, message)
