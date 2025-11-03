import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from passlib.context import CryptContext


class CryptoService:
    def __init__(
            self,
            iterations: int = 100_000,
            hash_algorithm=hashes.SHA256
    ):
        self._pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        self._iterations = iterations
        self._hash_algorithm = hash_algorithm

    def hash_password(self, password: str) -> str:
        """Хэширует пароль с помощью bcrypt"""
        return self._pwd_context.hash(password)

    def verify_password(
            self,
            plain_password: str,
            hashed_password: str
    ) -> bool:
        """Проверяет, что пароль совпадает с хэшем"""
        return self._pwd_context.verify(plain_password, hashed_password)

    def _gen_key_from_password(
            self,
            password: str,
            salt: bytes
    ) -> bytes:
        """Генерация ключа из пароля и соли"""
        password = password.encode()
        kdf = PBKDF2HMAC(
            algorithm=self._hash_algorithm(),
            length=32,
            salt=salt,
            iterations=self._iterations,
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    def encrypt_secret(
            self,
            message: str,
            password: str
    ) -> str:
        """Шифрует сообщение, возвращает hex( salt + ciphertext )"""
        salt = os.urandom(16)
        key = self._gen_key_from_password(password, salt)
        f = Fernet(key)
        encrypted_message = f.encrypt(message.encode())
        return (salt + encrypted_message).hex()

    def decrypt_secret(
            self,
            token: str,
            password: str
    ) -> str:
        """Дешифрует сообщение из hex"""
        bytes_token = bytes.fromhex(token)
        salt, encrypted_message = bytes_token[:16], bytes_token[16:]
        key = self._gen_key_from_password(password, salt)
        f = Fernet(key)
        return f.decrypt(encrypted_message).decode()


def crypto_service(
        iterations: int = 100_000,
        hash_algorithm=hashes.SHA256
) -> CryptoService:
    return CryptoService(iterations, hash_algorithm)