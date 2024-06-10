from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from binascii import unhexlify
from .interact_with_contract import *
import json


def verify_vc(w3, abi, contract_addr, vc):
    # 提取 VC 中的 proof
    did = vc["issuer"]
    proof = vc["proof"]
    proofValue = proof["proofValue"]
    algorithm = proof["type"]
    verification_method_id = proof["verificationMethod"]
    vc_copy = vc.copy()
    del vc_copy["proof"]
    json_bytes = json.dumps(vc_copy).encode()

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
        return True


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
            return False

        return True
    except InvalidSignature:
        return False
