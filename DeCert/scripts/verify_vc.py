import json
from brownie import DIDRegistry, accounts
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature


def base64url_decode(input):
    rem = len(input) % 4
    if rem > 0:
        input += '=' * (4 - rem)
    return base64.urlsafe_b64decode(input)


def verify_vc(vc):
    # 提取 VC 中的 proof
    proof = vc["proof"]
    jws = proof["jws"]
    signature_algorithm = proof["type"]
    verification_method_id = proof["verificationMethod"]

    # 分割 JWS
    parts = jws.split('.')
    if len(parts) != 3:
        return False, "Invalid JWS format"

    encoded_header, encoded_payload, encoded_signature = parts

    # 解码 JWS 头部和载荷
    header = json.loads(base64url_decode(encoded_header))
    payload = base64url_decode(encoded_payload)
    signature = base64url_decode(encoded_signature)

    # 从区块链上获取 DID 文档
    did_registry = DIDRegistry[-1]
    did_document_on_chain = did_registry.getDIDDocument(vc["issuer"])

    # 查找对应的 verificationMethod
    public_key_pem = None
    for vm in did_document_on_chain[5]:  # verificationMethods is the 6th element in the tuple
        if vm[0] == verification_method_id:
            public_key_pem = vm[2]
            break

    if public_key_pem is None:
        return False, "Verification method not found"

    # 加载公钥
    public_key = load_pem_public_key(public_key_pem.encode())

    # 验证签名
    try:
        if signature_algorithm == 'RsaSignature2018':
            public_key.verify(
                signature,
                f"{encoded_header}.{encoded_payload}".encode(),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
        elif signature_algorithm == 'EcdsaSecp256k1Signature2019':
            public_key.verify(
                signature,
                f"{encoded_header}.{encoded_payload}".encode(),
                ec.ECDSA(hashes.SHA256())
            )
        else:
            return False, f"Unsupported signature algorithm: {signature_algorithm}"

        return True, "Verification successful"
    except InvalidSignature:
        return False, "Invalid signature"

#
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
# result, message = verify_vc(vc)
# print(result, message)
