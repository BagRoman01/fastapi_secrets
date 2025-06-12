import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def gen_key_from_password(password: str, salt: bytes = b'salt_') -> bytes:
    password = password.encode()  # Convert to type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def encrypt_secret(message: str, password: str) -> str:
    salt = os.urandom(16)
    key = gen_key_from_password(password, salt)  # Generate key from password
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())  # Encrypt message
    return (salt + encrypted_message).hex()


def decrypt_secret(token: str, password: str) -> str:
    bytes_token = bytes.fromhex(token)
    salt = bytes_token[:16]
    encrypted_message = bytes_token[16:]
    key = gen_key_from_password(password, salt)  # Generate key from password
    f = Fernet(key)
    message = f.decrypt(encrypted_message)  # Decrypt message
    return message.decode()
