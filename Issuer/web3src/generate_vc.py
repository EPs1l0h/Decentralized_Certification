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
    elif algorithm.upper() == 'ECDSA' or algorithm.upper() == 'SM2':
        signature = private_key.sign(json_bytes, ec.ECDSA(hashes.SHA256()))
    else:
        raise UnsupportedAlgorithm(f'Unsupported algorithm: {algorithm}')

    return signature.hex()


def generate_vc(vc_type, issuer, credential_subject, key_id, private_key_pem, signature_algorithm):
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
        "type": ["VerifiableCredential", vc_type],
        "issuer": issuer,
        "issuanceDate": issuance_date,
        "credentialSubject": credential_subject,
    }

    # 对 VC 进行签名
    vc_data = json.dumps(vc).encode()
    proofValue = sign_json(vc_data, private_key_pem, signature_algorithm)

    # 构建 proof 对象
    proof = {
        "type": signature_algorithm,
        "created": datetime.now(timezone.utc).isoformat(),
        "proofPurpose": "assertionMethod",
        "verificationMethod": key_id,  # 假设公钥ID是 issuer/keys/1
        "proofValue": proofValue
    }

    # 将 proof 添加到 VC 中
    vc["proof"] = proof

    return vc
