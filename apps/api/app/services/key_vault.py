from dataclasses import dataclass
import base64
import binascii
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


@dataclass(frozen=True)
class EncryptedSecret:
    salt: str
    nonce: str
    ciphertext: str


def _derive_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390_000,
    )
    return kdf.derive(master_password.encode("utf-8"))


def encrypt_secret(master_password: str, secret: str) -> EncryptedSecret:
    if not master_password:
        raise ValueError("master password is required")
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = _derive_key(master_password, salt)
    ciphertext = AESGCM(key).encrypt(nonce, secret.encode("utf-8"), None)
    return EncryptedSecret(
        salt=base64.b64encode(salt).decode("ascii"),
        nonce=base64.b64encode(nonce).decode("ascii"),
        ciphertext=base64.b64encode(ciphertext).decode("ascii"),
    )


def decrypt_secret(master_password: str, encrypted: EncryptedSecret) -> str:
    try:
        salt = base64.b64decode(encrypted.salt, validate=True)
        nonce = base64.b64decode(encrypted.nonce, validate=True)
        ciphertext = base64.b64decode(encrypted.ciphertext, validate=True)
        key = _derive_key(master_password, salt)
        return AESGCM(key).decrypt(nonce, ciphertext, None).decode("utf-8")
    except (binascii.Error, InvalidTag, ValueError) as exc:
        raise ValueError("Unable to decrypt API key") from exc
