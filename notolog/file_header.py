"""
Notolog Editor
Open-source markdown editor developed in Python.

File Details:
- Purpose: File header class.
- Functionality: Stores and retrieves required and optional file data, as well as file state and parameters.

Repository: https://github.com/notolog/notolog-editor
Website: https://notolog.app
PyPI: https://pypi.org/project/notolog

Author: Vadim Bakhrenkov
Copyright: 2024 Vadim Bakhrenkov
License: MIT License

For detailed instructions and project information, please see the repository's README.md.
"""

import datetime
import logging
import json
import re
import os

from typing import Any, Union, Iterable
from json import JSONDecodeError

from .helpers.file_helper import read_file
from .encrypt.enc_helper import EncHelper

from .exceptions.file_header_empty_exception import FileHeaderEmptyException


class FileHeader:
    """
    File header stores the data about the file and its contents.
    Header is a line of data surrounded by HTML-comment tags to avoid having it visible on external resources.

    To avoid hassle the header is only appears in files created within the Notolog editor.
    Anyway, a header is required for encrypted files as it contains such important info as salt or other file data.
    """

    HEADER_TPL = '<!-- %s -->'

    def __init__(self):
        super(FileHeader, self).__init__()

        self.logger = logging.getLogger('header')

        self.logger.debug('Header helper is activated')

        self.header = None

    def get_new(self, is_enc: bool = False):
        if not self.header:
            self.header = self.generate(is_enc=is_enc)
        else:
            self.logger.warning('Attempt to create new file header on top of existing one!')
        return self

    def generate(self, is_enc: bool = False) -> json:
        created = updated = datetime.datetime.now()
        header = {'notolog.app': {'created': created, 'updated': updated}}
        if is_enc:
            header['notolog.app'].update(self.generate_enc())
        return header

    def generate_enc(self) -> json:
        return {'enc': {'slt': EncHelper.generate_salt(), 'itr': EncHelper.get_default_iterations(), 'hint': ''}}

    def set_encrypted(self):
        self.header['notolog.app'].update(self.generate_enc())

    def is_valid(self) -> bool:
        return (self.header is not None
                and isinstance(self.header, Iterable)
                and 'notolog.app' in self.header)

    def is_file_encrypted(self) -> bool:
        if not self.is_valid():
            return False
        _header = self.header['notolog.app']
        return 'enc' in _header and isinstance(_header['enc'], dict)

    def validate_enc(self) -> None:
        """
        Ensure that the header is valid and do migrations if necessary.
        """
        pass

    def refresh(self) -> None:
        date_now = datetime.datetime.now()
        # Update only existing header
        if self.is_valid():
            self.header['notolog.app']['updated'] = date_now
            if 'created' not in self.header['notolog.app'] or self.header['notolog.app']['created'] is None:
                self.header['notolog.app']['created'] = date_now
        else:
            self.logger.debug('File header is empty')

    def get_param(self, param: Any, default: Any = None) -> Union[str, dict, None]:
        """
        Get header's param by name.
        @param param: name of the param
        @param default: default value if param is not set or not found
        @return: either string or None
        """
        return (self.header['notolog.app'][param]
                if self.is_valid() and param in self.header['notolog.app']
                else default)

    def set_param(self, param: str, value: str) -> None:
        """
        Set params to the header.
        @param param: name of the param
        @param value: value of the param
        @return: None
        """
        if self.is_valid():
            self.header['notolog.app'][param] = value
        else:
            raise FileHeaderEmptyException()

    def get_enc_param(self, param: Any) -> Union[str, None]:
        """
        Get encryption related header's param by name.
        @param param: name of the param
        @return: either string or None
        """
        enc = self.get_param('enc')
        if enc and param in enc:
            return enc[param]
        return None

    def set_enc_param(self, param: str, value: str) -> None:
        """
        Set encryption params to the header.
        @param param: name of the param
        @param value: value of the param
        @return: None
        """
        enc = self.get_param('enc')
        if enc:
            enc.update({param: value})
            self.header['notolog.app'].update({'enc': enc})
        else:
            raise FileHeaderEmptyException()

    def pack(self, content: str = None, encode: bool = False) -> str:
        header_line = repr(self)
        delimiter = '\n'

        if encode:
            delimiter = delimiter.encode("utf-8")
            if header_line and type(header_line) is not bytes:
                header_line = header_line.encode("utf-8")
            if content is not None and type(content) is not bytes:
                content = content.encode("utf-8")

        if header_line and content is not None:
            # Return header and content, even if the content is empty
            return header_line + delimiter + content
        elif content is not None:
            self.logger.debug(f'File contains content but lacks a header {self}')
            # Return content without header
            return content
        else:
            self.logger.warning(f'File contains header but lacks a content {self}')
            # Return header without content
            return header_line

    def load_file(self, file_path: str) -> tuple[Any, str]:
        file_data = read_file(file_path)
        return self.load(file_data)

    def load(self, file_data: str) -> tuple[Any, Union[str, None]]:
        try:
            file_header_line = file_data.splitlines()[0]
        except (IndexError, AttributeError):
            self.logger.debug('File header is not found')
            return self, file_data

        self.header = None
        try:
            search = re.search(self.HEADER_TPL % '(.*?)', file_header_line, re.IGNORECASE)
            file_header_json = search.group(1) if search else None
            self.header = json.loads(file_header_json)
            # Run migrations here if needed
            self.validate_enc()
        except (TypeError, JSONDecodeError):
            self.logger.debug('File header is empty')
            return self, file_data

        if self.is_valid():
            # Splitting file_data into lines
            lines = file_data.splitlines()
            if len(lines) >= 2:
                file_body = "\n".join(lines[1:])
            else:
                file_body = None
            return self, file_body

        self.logger.debug('File header is empty')  # Suppose to be a valid situation if not set yet or not created

        return self, file_data

    def read(self, file_path: str) -> Union[str, None]:
        if os.path.isfile(file_path):
            with open(file_path, encoding='utf-8') as f:
                header_line = f.readline().strip('\n')
                return header_line
        else:
            self.logger.warning('File not found "%s"' % file_path)
        return None

    def __repr__(self) -> str:
        """
        Return header data as a formatted string
        """

        if self.header:
            return self.HEADER_TPL % json.dumps(self.header, default=str)

        return ''
