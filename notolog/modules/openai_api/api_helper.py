from PySide6.QtCore import QUrl, QByteArray
from PySide6.QtNetwork import QNetworkRequest

import json
import logging

from threading import Lock

from .. import AppConfig


class ApiHelper:

    _instance = None  # Singleton instance
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    # Create the instance if it doesn't exist
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        # Check if instance is already initialized
        if hasattr(self, 'logger'):
            return

        # Ensure that the initialization check and the setting of 'modules' param are atomic.
        with self._lock:
            # This prevents race conditions.
            if hasattr(self, 'logger'):
                return

            super(ApiHelper, self).__init__()

            self.parent = parent

            self.logger = logging.getLogger('openai_api_helper')

            self.logging = AppConfig().get_logging()
            self.debug = AppConfig().get_debug()

    def init_request(self, api_url, api_key) -> QNetworkRequest:

        url = QUrl(api_url)  # API entrypoint
        request = QNetworkRequest(url)

        # Set Authorization header
        request.setRawHeader(b"Authorization", bytes("Bearer " + api_key, encoding="utf-8"))

        # Set Content-Type header
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")

        # Set request type to POST
        request.setRawHeader(b"Custom-Request", b"POST")

        return request

    def init_request_params(self, prompt_messages, api_model,
                            # Optional arguments
                            options: dict = None) -> QByteArray:

        # New completions
        post_params = {
            "model": api_model,
            "messages": prompt_messages,
            "temperature": 0.2,
            "top_p": 1,
            "n": 1,
            "stream": False,
        }
        # If response max tokens set
        if 'response_max_tokens' in options:
            post_params.update({"max_tokens": options['response_max_tokens']})
        # Other params to override
        if 'temperature' in options:
            post_params.update({"temperature": options['temperature']})
        if 'top_p' in options:
            post_params.update({"top_p": options['top_p']})
        if 'n' in options:
            post_params.update({"n": options['n']})
        if 'stream' in options:
            post_params.update({"stream": bool(options['stream'])})

        json_post_params = json.dumps(post_params)

        # Set request data
        request_data = QByteArray(json_post_params.encode("utf-8"))

        return request_data

    # def get_prompt_from_text(self, text):
    #    prompt = f'{self.chat_template.format(input=text)}'
    #    return prompt
