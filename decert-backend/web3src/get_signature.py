import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import json

def load_private_key(private_key_pem, password=None):
    return load_pem_private_key(private_key_pem.encode(), password)

def sign_with_rsa(private_key, message):
    signature = private_key.sign(
        message,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature

def sign_with_sm2(private_key, message):
    signature = private_key.sign(
        message,
        ec.ECDSA(hashes.SHA256())
    )
    return signature

def Signature(did_document, type_of_proof, private_key_pem):
    # Load the DID document
    del did_document["proof"]
    did_document_json = json.dumps(did_document)
    message = did_document_json.encode()
    print("message_did: ", message)
    # Load the private key
    private_key = load_private_key(private_key_pem)

    # Sign the message based on the type of proof
    if type_of_proof == "RSA":
        signature = sign_with_rsa(private_key, message)
    elif type_of_proof == "SM2":
        signature = sign_with_sm2(private_key, message)
    else:
        raise ValueError(f"Unsupported type_of_proof: {type_of_proof}")

    return signature.hex()
