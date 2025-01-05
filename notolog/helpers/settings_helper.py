"""
Notolog Editor
An open-source Markdown editor built with Python.

File Details:
- Purpose: Settings helper class.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024-2025 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken, InvalidSignature

from . import AppConfig

from typing import Any, Union

import os
import logging


class SettingsHelper:
    """
    Settings helper to perform additional operations like encrypting/decrypting sensitive data with
    symmetric encryption algorithm to store it in settings, as settings file may be exposed.
    """

    env_secret_name = "NOTOLOG_APP_SECRET_KEY"

    def __init__(self):
        super().__init__()

        self.logger = logging.getLogger('settings_helper')

        self.logger.info('Settings helper is activated')

        self.key = self.get_app_key()

    def encrypt_data(self, data) -> Union[str, None]:
        if not data:
            return data  # Empty default
        data_encoded = data.encode('utf-8')
        try:
            # Encrypt data using Fernet symmetric encryption.
            cipher_suite = Fernet(self.key)
            encrypted_data = cipher_suite.encrypt(data_encoded)
            return encrypted_data.decode('utf-8')
        except (InvalidToken, InvalidSignature, TypeError) as e:
            self.logger.warning(f'Settings helper encryption token error: {e}')
        except Exception as e:
            self.logger.warning(f'An unexpected error occurred while encrypting data: {e}')
        return None

    def decrypt_data(self, encrypted_data: Any) -> Union[str, None]:
        if not encrypted_data:
            # When settings not set
            return encrypted_data  # Empty default
        if not isinstance(encrypted_data, bytes):
            encrypted_data = encrypted_data.encode('utf-8')
        try:
            # Decrypt data using Fernet symmetric encryption.
            cipher_suite = Fernet(self.key)
            decrypted_data = cipher_suite.decrypt(encrypted_data)
            return decrypted_data.decode('utf-8')
        except (InvalidToken, InvalidSignature, TypeError) as e:
            self.logger.warning(f'Settings helper encryption token error: {e}')
        except Exception as e:
            self.logger.warning(f'An unexpected error occurred while decrypting data: {e}')
        return None

    def get_app_key(self) -> bytes:
        # Get the key from the system env first
        app_key_str = os.getenv(self.env_secret_name)

        # Trying to access key via the app config
        if app_key_str is None:
            app_key_str = AppConfig().get_security_app_secret()
            if app_key_str:
                # Store key with system envs
                os.environ[self.env_secret_name] = app_key_str

        # If no key found create a new one
        if not app_key_str:
            self.logger.info("Creating app new secret key")
            # Generate app new key. This is a base64-encoded bytes string
            app_key = self.generate_app_key()
            # Set up app new key
            self.setup_app_key(app_key)
            # Return new 32 url-safe base64-encoded bytes key
            return app_key
        else:
            # Convert the retrieved string back to bytes
            return app_key_str.encode('ascii')

    def setup_app_key(self, app_key: bytes) -> None:
        # Convert bytes to a string (decoding by ASCII)
        app_key_str = app_key.decode('ascii')
        # Store key in system envs
        os.environ[self.env_secret_name] = app_key_str
        # Store key in app config
        AppConfig().set_security_app_secret(app_key_str)

    @staticmethod
    def generate_app_key() -> bytes:
        # Generate a key without password, for app needs.
        return Fernet.generate_key()

    def _recreate_app_key(self):
        """
        Proof-of-Concept method; Avoid to use it in scenarios different from data repairing.
        """
        _new_app_key = self.generate_app_key()
        self.setup_app_key(_new_app_key)
        self.key = _new_app_key
        # Update settings value(s) upon that
        # value = self.encrypt_data(value)
        # settings.setValue(param_name, value)

    def parse_object_name(self, object_name: str) -> list:
        if object_name.__contains__(":"):
            object_name_parts = object_name.split(":")
            if len(object_name_parts) == 2:
                # lexeme_key, setting_name
                return object_name_parts
            else:
                self.logger.warning(f"Object name in a wrong format '{object_name}'")
        else:
            # lexeme_key, setting_name
            return [object_name, object_name]
