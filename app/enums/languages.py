from enum import Enum


class Languages(Enum):

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Override _generate_next_value_ to allow for custom attributes on enum members (mostly for default).
        """
        return name, False  # The second value in the tuple is the custom attribute indicating whether it's the default

    DE = "German"
    EN = ("English", True)
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
    PT = "Portuguese"
    RU = "Russian"
    SE = "Swedish"
    TR = "Turkish"
    ZH = "Chinese"

    def __init__(self, value, is_default=False):
        self._value_ = value
        self.is_default = is_default

    def __str__(self):
        return self.name.lower()

    @classmethod
    def __getitem__(cls, key):
        if isinstance(key, str):
            key = key.upper()  # Normalize the key to uppercase
        return cls._member_map_[key]

    @classmethod
    def default(cls):
        """
        Returns the default value of the Enum.
        Usage:
            self.default()
        @return: Any
        """
        # Find and return the default enum member
        for member in cls:
            if member.is_default:
                return member
        return None  # If no default is marked, return None or consider raising an error
