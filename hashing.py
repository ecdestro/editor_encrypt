import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

user = input()
password = user.encode()
salt = b'\xc1\x17W\xad\x18?b\xb1\x999\x8cJ0\xa8\\j'
kdf = PBKDF2HMAC(
    algorithm = hashes.SHA512(),
    length = 32,
    salt = salt,
    iterations = 100000,
    backend = default_backend()
)

key = base64.urlsafe_b64encode(kdf.derive(password))
print(key)