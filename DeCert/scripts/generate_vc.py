import json
import uuid
import base64
from datetime import datetime, timezone
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa, ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import utils as asym_utils
from cryptography.hazmat.backends import default_backend


def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')


def sign_vc_data(vc_data, private_key_pem, signature_algorithm):
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

    # 编码 VC 数据
    encoded_payload = base64url_encode(vc_data)

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


def generate_vc(vc_type, issuer, credential_subject, private_key_pem,
                            signature_algorithm='RsaSignature2018'):
    # 定义 context
    context = "https://www.w3.org/2018/credentials/v1"

    # 生成唯一的证书ID
    vc_id = f"DeCertIssuer-{uuid.uuid4()}"

    # 获取当前时间作为发行时间
    issuance_date = datetime.now(timezone.utc).isoformat()

    # 构建 VC 证书
    vc = {
        "@context": context,
        "id": vc_id,
        "type": ["VerifiableCredential"] + vc_type,
        "issuer": issuer,
        "issuanceDate": issuance_date,
        "credentialSubject": credential_subject,
    }

    # 对 VC 进行签名
    vc_data = json.dumps(vc, separators=(',', ':')).encode()
    jws = sign_vc_data(vc_data, private_key_pem, signature_algorithm)

    # 构建 proof 对象
    proof = {
        "type": signature_algorithm,
        "created": datetime.now(timezone.utc).isoformat(),
        "proofPurpose": "assertionMethod",
        "verificationMethod": f"{issuer}/keys/1",  # 假设公钥ID是 issuer/keys/1
        "jws": jws
    }

    # 将 proof 添加到 VC 中
    vc["proof"] = proof

    return vc
#
#
# # 示例输入
# vc_type = ["AlumniCredential"]
# issuer = "https://example.edu/issuers/565049"
# credential_subject = {
#     "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
#     "alumniOf": {
#         "id": "did:example:c276e12ec21ebfeb1f712ebc6f1",
#         "value": "Example University",
#         "lang": "en"
#     }
# }
#
# # 示例私钥（PEM 格式）
# private_key_pem = """
# -----BEGIN RSA PRIVATE KEY-----
# MIIEpAIBAAKCAQEA1X1+zO2+Zs3Pj5F9Z9zj6K5FQ5U5v+F2Z2Y5Q5Y5d5Y5F5W5
# ...
# -----END RSA PRIVATE KEY-----
# """
#
# # 生成 VC 证书
# vc_certificate = generate_vc(vc_type, issuer, credential_subject, private_key_pem)
#
# # 打印生成的 VC 证书
# print(json.dumps(vc_certificate, indent=2))
