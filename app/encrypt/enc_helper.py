from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

from .enc_password import EncPassword

from . import AppConfig
from . import Settings

import logging
import secrets
import base64

from typing import Union


class EncHelper:
    """
    Encrypt/decrypt file data with symmetric encryption algorithm
    """

    """
    Adjust the number of iterations for more security.
    Remember to re-encrypt the source.
    """
    DEFAULT_ITERATIONS = 768000

    def __init__(self, enc_password: EncPassword = None, salt: str = None, iterations: int = None):
        super().__init__()

        self.logging = AppConfig.get_logging()
        self.debug = AppConfig.get_debug()

        self.logger = logging.getLogger('enc_helper')

        self.enc_password = enc_password
        self.salt = salt
        self.iterations = iterations

        if self.enc_password is not None:
            self.password = self.enc_password.password if self.enc_password.password is not None else ''
        else:
            if self.logging:
                self.logger.warning('No password provided! Unsecure result')
            self.enc_password = EncPassword()
            self.enc_password.password = self.password = ''

        if type(self.password) is not bytes:
            self.password = self.password.encode()

        if self.salt is None:
            if self.logging:
                self.logger.warning('No salt provided! Random value generated')
            self.salt = self.generate_salt()

        if type(self.salt) is not bytes:
            self.salt = self.salt.encode()

        if self.iterations is None:
            if self.logging:
                self.logger.warning('No iterations provided! Default value fallback')
            self.iterations = self.__class__.get_default_iterations()

        # Derive key from password
        key = self.generate_key_from_password()
        encoded_key = base64.urlsafe_b64encode(key)
        # Fernet uses only the first 128 bits (16 bytes) of the key for AES encryption.
        self.cipher_suite = Fernet(encoded_key)

        self.key = None

    def generate_key_from_password(self) -> bytes:
        """
        Generate a key from the password

        Password-Based Key Derivation Function 2 (PBKDF2) implementation.
        The param length=32 is the length of the derived key.
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            iterations=self.iterations,
            salt=self.salt,
            length=32  # 32 bytes = 256 bits key
        )

        self.key = kdf.derive(self.password)

        return self.key

    @staticmethod
    def generate_key() -> bytes:
        """
        Generate a key without password, just in case
        """
        return Fernet.generate_key()

    def encrypt_data(self, source_data: bytes) -> Union[bytes, None]:
        """
        Encrypt the data.
        This method can be called when no real password was set due cancellation.
        """
        if not self.is_password_valid():
            return None
        return self.cipher_suite.encrypt(source_data)

    def decrypt_data(self, encrypted_data: bytes) -> Union[bytes, None]:
        """
        Decrypt the data.
        This method can be called when no real password was set due to cancellation.
        """
        if not self.is_password_valid():
            return None
        return self.cipher_suite.decrypt(encrypted_data)

    def is_password_valid(self) -> bool:
        """
        Check either the password is valid or not
        """
        return self.password is not None and len(self.password) > 0

    @staticmethod
    def generate_salt(length: int = 32) -> str:
        """
        Generate new salt static method
        """
        return secrets.token_urlsafe(length)

    @staticmethod
    def get_default_iterations() -> int:
        # Allow update default value and store it in settings
        settings = Settings()
        # Return number of iterations from settings, or use the default fallback to update it
        if not settings.enc_iterations:
            # If settings value wasn't initiated
            settings.enc_iterations = EncHelper.DEFAULT_ITERATIONS
        return int(settings.enc_iterations)
