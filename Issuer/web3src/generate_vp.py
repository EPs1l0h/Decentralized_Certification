import json
import uuid
import base64
from datetime import datetime, timezone
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.exceptions import UnsupportedAlgorithm

def sign_json(json_bytes, private_key_pem, algorithm):
    # Load the private key from PEM
    private_key = load_pem_private_key(private_key_pem.encode(), password=None)

    if algorithm.upper() == 'RSA':
        signature = private_key.sign(
            json_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
    elif algorithm.upper() == 'ECDSA':
        signature = private_key.sign(json_bytes, ec.ECDSA(hashes.SHA256()))
    else:
        raise UnsupportedAlgorithm(f'Unsupported algorithm: {algorithm}')

    return signature.hex()

def generate_vp(type, verifiable_credential, private_key_pem, signature_algorithm, verification_method):
    # 定义 context
    context = [
        "https://www.w3.org/2018/credentials/v1",
        "https://www.w3.org/2018/credentials/examples/v1"
    ]

    # 生成唯一的挑战值 (challenge) 和域 (domain)
    challenge = str(uuid.uuid4())
    domain = "example.com"

    # 构建 VP
    vp = {
        "@context": context,
        "type": type,
        "verifiableCredential": verifiable_credential
    }

    # 对 VP 进行签名
    vp_data = json.dumps(vp).encode()
    proofValue = sign_json(vp_data, private_key_pem, signature_algorithm)

    # 构建 proof 对象
    proof = {
        "type": signature_algorithm,
        "created": datetime.now(timezone.utc).isoformat(),
        "proofPurpose": "authentication",
        "verificationMethod": verification_method,
        "challenge": challenge,
        "domain": domain,
        "proofValue": proofValue
    }

    # 将 proof 添加到 VP 中
    vp["proof"] = proof

    return vp
#
#
# # 示例输入
# type = ["VerifiablePresentation"]
# verifiable_credential = [{
#     "@context": "https://www.w3.org/2018/credentials/v1",
#     "id": "http://example.edu/credentials/1872",
#     "type": ["VerifiableCredential", "AlumniCredential"],
#     "issuer": "https://example.edu/issuers/565049",
#     "issuanceDate": "2010-01-01T19:73:24Z",
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
#         "created": "2017-06-18T21:19:10Z",
#         "proofPurpose": "assertionMethod",
#         "verificationMethod": "https://example.edu/issuers/keys/1",
#         "jws": "eyJhbGciOiJSUzI1NiIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il19..TCYt5XsITJX1CxPCT8yAV-TVkIEq_PbChOMqsLfRoPsnsgw5WEuts01mq-pQy7UJiN5mgRxD-WUcX16dUEMGlv50aqzpqh4Qktb3rk-BuQy72IFLOqV0G_zS245-kronKb78cPN25DGlcTwLtjPAYuNzVBAh4vGHSrQyHUdBBPM"
#     }
# }]
#
# # 示例私钥（PEM 格式）
# private_key_pem = """
# -----BEGIN RSA PRIVATE KEY-----
# MIIEpAIBAAKCAQEA1X1+zO2+Zs3Pj5F9Z9zj6K5FQ5U5v+F2Z2Y5Q5Y5d5Y5F5W5
# ...
# -----END RSA PRIVATE KEY-----
# """
#
# # 生成 VP
# vp = generate_vp(type, verifiable_credential, private_key_pem)
#
# # 打印生成的 VP
# print(json.dumps(vp, indent=2))