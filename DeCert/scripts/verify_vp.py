import json
import base64
from datetime import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature


def base64url_decode(input):
    rem = len(input) % 4
    if rem > 0:
        input += '=' * (4 - rem)
    return base64.urlsafe_b64decode(input)


def verify_signature(jws, public_key_pem, signature_algorithm):
    parts = jws.split('.')
    if len(parts) != 3:
        return False, "Invalid JWS format"

    encoded_header, encoded_payload, encoded_signature = parts

    header = json.loads(base64url_decode(encoded_header))
    payload = base64url_decode(encoded_payload)
    signature = base64url_decode(encoded_signature)

    public_key = load_pem_public_key(public_key_pem.encode())

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


def verify_vc(vc):
    proof = vc["proof"]
    jws = proof["jws"]
    signature_algorithm = proof["type"]
    verification_method_id = proof["verificationMethod"]

    # 从链上获取 DID 文档
    did_registry = DIDRegistry[-1]
    did_document_on_chain = did_registry.getDIDDocument(vc["issuer"])

    public_key_pem = None
    for vm in did_document_on_chain[5]:
        if vm[0] == verification_method_id:
            public_key_pem = vm[2]
            break

    if public_key_pem is None:
        return False, "Verification method not found"

    return verify_signature(jws, public_key_pem, signature_algorithm)


def verify_vp(vp):
    proof = vp["proof"]
    jws = proof["jws"]
    signature_algorithm = proof["type"]
    verification_method_id = proof["verificationMethod"]

    # 验证包含的每一个 VC
    for vc in vp["verifiableCredential"]:
        result, message = verify_vc(vc)
        if not result:
            return False, f"VC verification failed: {message}"

    # 从链上获取 DID 文档
    did_registry = DIDRegistry[-1]
    did_document_on_chain = did_registry.getDIDDocument(verification_method_id.split('#')[0])

    public_key_pem = None
    for vm in did_document_on_chain[5]:
        if vm[0] == verification_method_id:
            public_key_pem = vm[2]
            break

    if public_key_pem is None:
        return False, "Verification method not found"

    return verify_signature(jws, public_key_pem, signature_algorithm)
#
#
# # 示例 VP
# vp = {
#     "@context": [
#         "https://www.w3.org/2018/credentials/v1",
#         "https://www.w3.org/2018/credentials/examples/v1"
#     ],
#     "type": "VerifiablePresentation",
#     "verifiableCredential": [{
#         "@context": "https://www.w3.org/2018/credentials/v1",
#         "id": "http://example.edu/credentials/1872",
#         "type": ["VerifiableCredential", "AlumniCredential"],
#         "issuer": "https://example.edu/issuers/565049",
#         "issuanceDate": "2010-01-01T19:73:24Z",
#         "credentialSubject": {
#             "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
#             "alumniOf": {
#                 "id": "did:example:c276e12ec21ebfeb1f712ebc6f1",
#                 "value": "Example University",
#                 "lang": "en"
#             }
#         },
#         "proof": {
#             "type": "RsaSignature2018",
#             "created": "2017-06-18T21:19:10Z",
#             "proofPurpose": "assertionMethod",
#             "verificationMethod": "https://example.edu/issuers/keys/1",
#             "jws": "eyJhbGciOiJSUzI1NiIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il19..TCYt5XsITJX1CxPCT8yAV-TVkIEq_PbChOMqsLfRoPsnsgw5WEuts01mq-pQy7UJiN5mgRxD-WUcX16dUEMGlv50aqzpqh4Qktb3rk-BuQy72IFLOqV0G_zS245-kronKb78cPN25DGlcTwLtjPAYuNzVBAh4vGHSrQyHUdBBPM"
#         }
#     }],
#     "proof": {
#         "type": "RsaSignature2018",
#         "created": "2018-09-14T21:19:10Z",
#         "proofPurpose": "authentication",
#         "verificationMethod": "did:example:ebfeb1f712ebc6f1c276e12ec21#keys-1",
#         "challenge": "1f44d55f-f161-4938-a659-f8026467f126",
#         "domain": "4jt78h47fh47",
#         "jws": "eyJhbGciOiJSUzI1NiIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il19..kTCYt5XsITJX1CxPCT8yAV-TVIw5WEuts01mq-pQy7UJiN5mgREEMGlv50aqzpqh4Qq_PbChOMqsLfRoPsnsgxD-WUcX16dUOqV0G_zS245-kronKb78cPktb3rk-BuQy72IFLN25DYuNzVBAh4vGHSrQyHUGlcTwLtjPAnKb78"
#     }
# }
#
# # 验证 VP
# result, message = verify_vp(vp)
# print(result, message)
