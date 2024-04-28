from enum import Enum


class AiModelNames(Enum):

    # Override _generate_next_value_ to allow for custom attributes on enum members (mostly for default).
    def _generate_next_value_(name, start, count, last_values):
        """
        'name' is the name of the Enum's member, which will be 'A', 'B', 'C', etc.
        This method returns the name itself, a 'default' marker (False), and a 'legacy' marker (False)
        """
        return name, False, False

    GPT_3_5 = ("gpt-3.5-turbo", True)  # The second item in the tuple marks this as the default
    GPT_3_5_LEGACY = ("gpt-3.5-turbo-instruct", False, True)  # Third param is a legacy flag (e.g. legacy completions)

    def __init__(self, value, is_default=False, legacy=False):
        # If the value is a tuple, unpack it.
        if isinstance(value, tuple):
            self._value_, self.is_default, self.legacy = value
        else:
            self._value_ = value
            self.is_default = is_default
            self.legacy = legacy

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

    @classmethod
    def legacy_members(cls):
        return [member for member in cls if member.legacy]

    @classmethod
    def legacy(cls, member):
        return member in cls.legacy_members()
