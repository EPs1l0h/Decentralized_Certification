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
