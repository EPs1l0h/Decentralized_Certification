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
# #
# #
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
# b_dir = os.path.dirname(os.path.abspath(__file__))
# c_path = os.path.join(b_dir, 'contract_address.txt')
# with open (c_path,'r') as file:
#     contract_address = file.read()
# print(contract_address)
# result, message = verify_vp(vp,contract_address,vp["verifiableCredential"][0]["credentialSubject"]["id"])
# print(result, message)
