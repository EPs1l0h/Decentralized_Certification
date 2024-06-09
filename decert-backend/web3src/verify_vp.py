from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature
from .interact_with_contract import *
from .verify_vc import verify_vc

def verify_vp(w3, abi, contract_addr, vp):
    proof = vp["proof"]
    proofValue = proof["proofValue"]
    algorithm = proof["type"]
    verification_method_id = proof["verificationMethod"]
    did = verification_method_id.split('#')[0]
    vp_copy = vp.copy()
    del vp_copy["proof"]
    json_bytes = json.dumps(vp_copy).encode()

    # 验证包含的每一个 VC
    for vc in vp["verifiableCredential"]:
        vc_document = json.loads(vc)
        result = verify_vc(w3, abi, contract_addr, vc_document)
        if not result:
            return False

    # 从链上获取 DID 文档
    did_document_on_chain = get_did_document(w3, abi, contract_addr, did)

    public_key_pem = None
    for vm in did_document_on_chain[5]:
        if vm[0] == verification_method_id:
            public_key_pem = vm[2]
            break

    if public_key_pem is None:
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