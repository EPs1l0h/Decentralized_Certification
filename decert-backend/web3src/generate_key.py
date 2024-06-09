from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption, PublicFormat


def generate_keys(alg_type):
    if alg_type == 'RSA':
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()
    elif alg_type == 'SM2':
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()
    else:
        print('Error: Invalid algorithm type. Please enter RSA or SM2')

    # Serializing the keys to PEM format
    pem_private_key = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption()
    ).decode()

    pem_public_key = public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo
    ).decode()

    return pem_private_key, pem_public_key