import os
import logging
import importlib.util

from typing import Union, Dict

from ..enums.languages import Languages


class Lexemes:
    def __init__(self, language: str = 'en', default_scope: str = 'common', lexemes_dir: str = None):
        if not language or language in ('.', '..'):
            # Default language ('en')
            language = str(Languages.default())

        self.language = language
        self._default_scope = default_scope
        self._lexemes_dir = lexemes_dir

        # Lexeme storage
        self.lexemes = {}

        self.logger = logging.getLogger('lexemes')

        self.lexemes = self.load_lexemes()

    def get_lexemes_dir(self):
        # Check if lexemes dir is re-written
        lexemes_dir = self._lexemes_dir if self._lexemes_dir else os.path.dirname(__file__)
        # Lexemes dir for the selected language
        lexemes_lang_dir = os.path.join(lexemes_dir, self.language)
        if not os.path.isdir(lexemes_lang_dir):
            # Default language ('en')
            lexemes_lang_dir = os.path.join(lexemes_dir, str(Languages.default()))
        return lexemes_lang_dir

    def load_lexemes(self) -> Dict[str, Dict]:
        # Get the directory path of lexemes relative to this file
        lexemes_lang_dir = self.get_lexemes_dir()

        lexeme_files = []
        if os.path.isdir(lexemes_lang_dir):
            for file_name in os.listdir(lexemes_lang_dir):
                # Load all .py files from the dir excluding __init__.py file if exists
                if file_name.endswith('.py') and file_name != '__init__.py':
                    lexeme_files.append(os.path.join(lexemes_lang_dir, file_name))

        # Import and collect lexemes from each lexeme file
        lexemes = {}
        for file_path in lexeme_files:
            scope_name = os.path.splitext(os.path.basename(file_path))[0]
            if scope_name not in lexemes:
                lexemes[scope_name] = {}
            spec = importlib.util.spec_from_file_location(scope_name, file_path)
            lexemes_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(lexemes_module)
            if hasattr(lexemes_module, 'lexemes'):
                lexemes[scope_name].update(lexemes_module.lexemes)

        return lexemes

    def set_language(self, language: str) -> None:
        """
        Set language and re-load all corresponded lexemes
        @param language: string key of the language to load
        @return: None
        """
        self.language = language
        self.load_lexemes()

    def get(self, name, scope: str = None, **kwargs) -> Union[str, None]:
        """
        Get lexeme by its name and scope (optional; default 'common')
        @param name: lexeme's name key
        @param scope: lexeme's scope, e.g. common, encrypt, etc. If not set default_scope is in use.
        @return: either string value or None if lexeme's scope is not found
        """
        if not scope:
            # Use this method to get default scope as it may contain extra logic
            scope = self.get_default_scope()

        lexeme = self.lexemes[scope].get(name, '') if scope in self.lexemes else None
        if isinstance(lexeme, bytes):
            lexeme = lexeme.decode('utf-8')

        if kwargs:
            # Process placeholders if set, e.g. name="abc" in a string like "... {name} ..." become "... abc ..."
            try:
                lexeme = lexeme.format(**kwargs)
            except AttributeError:
                self.logger.warning('Lexeme "%s" not found' % name)
            except KeyError:
                self.logger.warning('Lexeme "%s" params [%s] not found for replacement'
                                    % (lexeme, ', '.join(kwargs.keys())))
        return lexeme

    def get_all(self):
        # Return all lexemes set
        return self.lexemes

    def get_default_scope(self):
        # Default scope if set
        scope = self._default_scope

        # If scope is not found in loaded lexemes
        if scope not in self.lexemes:
            # The very last fallback option
            scope = 'common'

        return scope

    def get_full_key(self, name, scope: str = None):
        if not scope:
            # Use this method to get default scope as it may contain extra logic
            scope = self.get_default_scope()

        return f"{scope}_{name}"
