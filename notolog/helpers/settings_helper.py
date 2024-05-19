from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken, InvalidSignature

from . import AppConfig

from typing import Union

import os
import logging
import base64


class SettingsHelper:
    """
    Settings helper to perform additional operations like encrypting/decrypting sensitive data with
    symmetric encryption algorithm to store it in settings, as settings file may be exposed.
    """

    def __init__(self):
        super().__init__()

        self.logger = logging.getLogger('settings_helper')

        self.logging = AppConfig().get_logging()  # TODO check
        self.debug = AppConfig().get_debug()

        if self.debug:
            self.logger.info('Settings helper is engaged')

        self.key = self.get_app_key()

    def encrypt_data(self, data) -> Union[str, None]:
        try:
            # Encrypt data using Fernet symmetric encryption.
            cipher_suite = Fernet(self.key)
            encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
            return encrypted_data.decode('utf-8')
        except (InvalidToken, InvalidSignature, TypeError) as e:
            if self.logging:
                self.logger.warning(f'Settings helper encryption token error: {e}')
        return None

    def decrypt_data(self, encrypted_data: bytes) -> Union[str, None]:
        try:
            # Decrypt data using Fernet symmetric encryption.
            cipher_suite = Fernet(self.key)
            decrypted_data = cipher_suite.decrypt(encrypted_data)
            return decrypted_data.decode('utf-8')
        except (InvalidToken, InvalidSignature, TypeError) as e:
            if self.logging:
                self.logger.warning(f'Settings helper encryption token error: {e}')
        return None

    def get_app_key(self) -> bytes:
        # Get the key from the system env first
        app_key = os.getenv("NOTOLOG_APP_SECRET_KEY")

        # Trying to access key via the app config
        if app_key is None:
            app_key = AppConfig().get_security_app_secret()
            if app_key:
                # Store key with system envs
                os.environ["NOTOLOG_APP_SECRET_KEY"] = app_key

        # If no key found create a new one
        if not app_key:
            if self.logging:
                self.logger.info("Creating app new secret key")
            # Generate app new key
            app_key = self.generate_app_key()
            # Encode this binary data to a Base64 string (still bytes)
            encoded_key = base64.urlsafe_b64encode(app_key)
            # Convert bytes to a string (decoding by ASCII)
            encoded_key_str = encoded_key.decode('ascii')
            # Store key in system envs
            os.environ["NOTOLOG_APP_SECRET_KEY"] = encoded_key_str
            # Store key in app config
            AppConfig().set_security_app_secret(encoded_key_str)
            # Return new key
            return app_key
        else:
            # Convert the retrieved string back to bytes
            app_key_bytes = app_key.encode('ascii')
            # Decode the Base64 bytes back to the original binary data
            return base64.urlsafe_b64decode(app_key_bytes)

    @staticmethod
    def generate_app_key() -> bytes:
        # Generate a key without password, for app needs.
        return Fernet.generate_key()
