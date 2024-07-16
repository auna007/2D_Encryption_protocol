### 1. Generating ECDSA Keys and Signing/Verifying

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature

# Generate ECDSA Key Pair
curve = ec.SECP224R1()
private_key = ec.generate_private_key(curve, default_backend())
public_key = private_key.public_key()

# Signing with ECDSA
message = b"Hello, World!"
signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))

# Verifying the signature
try:
    public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
    print("Signature verified successfully.")
except InvalidSignature:
    print("Invalid signature.")


### 2. Diffie-Hellman Key Exchange

import os
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

# Generate Diffie-Hellman parameters
parameters = dh.generate_parameters(generator=2, key_size=512, backend=default_backend())

# Generate DH key pair
private_key = parameters.generate_private_key()
public_key = private_key.public_key()

# Serialize DH public key
dh_pub_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
print(dh_pub_key_bytes.decode())

# In Python, we typically don't need to explicitly specify parameters for KeyPairGenerator
# The key pair is generated directly from the DH parameters generated above.

### 3. AES Encryption/Decryption Using ECDH Shared Secret

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import b64encode, b64decode
from io import BytesIO
import os

class AESSecurityCap:
    def __init__(self):
        self.private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        self.public_key = self.private_key.public_key()
        self.shared_key = None
        self.peer_public_key = None

    def generate_public_key(self):
        return self.public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

    def compute_shared_key(self, peer_public_key_bytes):
        peer_public_key = serialization.load_pem_public_key(peer_public_key_bytes, backend=default_backend())
        self.shared_key = self.private_key.exchange(ec.ECDH(), peer_public_key)

    def encrypt(self, plaintext):
        if not self.shared_key:
            raise ValueError("Shared key has not been computed.")

        iv = os.urandom(16)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
            backend=default_backend()
        ).derive(self.shared_key)
        aesgcm = AESGCM(derived_key)
        ciphertext = aesgcm.encrypt(iv, plaintext.encode(), None)
        return b64encode(iv + ciphertext).decode()

    def decrypt(self, ciphertext):
        if not self.shared_key:
            raise ValueError("Shared key has not been computed.")

        ciphertext = b64decode(ciphertext.encode())
        iv = ciphertext[:16]
        ciphertext = ciphertext[16:]

        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
            backend=default_backend()
        ).derive(self.shared_key)
        aesgcm = AESGCM(derived_key)
        plaintext = aesgcm.decrypt(iv, ciphertext, None)
        return plaintext.decode()



# This Python code uses the cryptography library, which is a robust 
# library for cryptographic operations in Python. It provides similar
# functionalities to the Java code you provided, including generating 
# keys, signing with ECDSA, Diffie-Hellman key exchange, and AES 
# encryption/decryption using ECDH shared secrets.