import json
import uuid
import base64
from datetime import datetime, timezone
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa, ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')


def sign_vp_data(vp_data, private_key_pem, signature_algorithm):
    # 加载私钥
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None,
        backend=default_backend()
    )

    # 构建 JWS 头部
    header = {
        "alg": "RS256" if signature_algorithm == 'RsaSignature2018' else "ES256K",
        "typ": "JWT"
    }
    encoded_header = base64url_encode(json.dumps(header).encode())

    # 编码 VP 数据
    encoded_payload = base64url_encode(vp_data)

    # 生成签名输入
    signing_input = f"{encoded_header}.{encoded_payload}".encode()

    # 根据签名算法选择签名方法
    if signature_algorithm == 'RsaSignature2018':
        signature = private_key.sign(
            signing_input,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
    elif signature_algorithm == 'EcdsaSecp256k1Signature2019':
        signature = private_key.sign(
            signing_input,
            ec.ECDSA(hashes.SHA256())
        )
    else:
        raise ValueError(f"Unsupported signature algorithm: {signature_algorithm}")

    encoded_signature = base64url_encode(signature)

    # 返回 JWS
    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"


def generate_vp(type, verifiable_credential, private_key_pem, signature_algorithm='RsaSignature2018',
                verification_method='did:example:ebfeb1f712ebc6f1c276e12ec21#keys-1'):
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
    vp_data = json.dumps(vp, separators=(',', ':')).encode()
    jws = sign_vp_data(vp_data, private_key_pem, signature_algorithm)

    # 构建 proof 对象
    proof = {
        "type": signature_algorithm,
        "created": datetime.now(timezone.utc).isoformat(),
        "proofPurpose": "authentication",
        "verificationMethod": verification_method,
        "challenge": challenge,
        "domain": domain,
        "jws": jws
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
