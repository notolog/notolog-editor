from PySide6.QtCore import QLocale

from .enum_base import EnumBase

assert hasattr(EnumBase, 'default'), "Check default() method is implemented in the base class"


class Languages(EnumBase):

    DE = "German"
    EN = ("English", True)  # Fallback default option
    ES = "Spanish"
    FI = "Finnish"
    FR = "French"
    GE = "Georgian"
    GR = "Greek"
    IN = "Hindi"
    IT = "Italian"
    JA = "Japanese"
    KO = "Korean"
    LA = "Latin"
    NL = "Dutch"
    PT = "Portuguese"
    RU = "Russian"
    SE = "Swedish"
    TR = "Turkish"
    ZH = "Chinese"

    def __init__(self, value, is_default=False):
        self._value_ = value
        self.is_default = is_default

    @classmethod
    def default(cls):
        """
        Returns the default value of the Enum.
        Usage:
            self.default()
        @return: Any
        """

        locale = QLocale.system()  # Get the system's locale
        iso_language_code = locale.name().split('_')[0]  # Extract the language part and ignore the country part

        # Find and return the default enum member based on the system locale
        for member in cls:
            # System locale as a default locale
            if iso_language_code and member.name.lower() == iso_language_code:
                return member

        # Fallback to the parent's logic
        return super().default()
