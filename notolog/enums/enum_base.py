from enum import Enum


class EnumBase(Enum):

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Override _generate_next_value_ to allow for custom attributes on enum members (mostly for default).

        'name' is the name of the Enum's member, which will be 'A', 'B', 'C', etc.
        This method returns the name itself and a 'default' marker (False)
        """
        return name, False

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
            if hasattr(member, 'is_default') and member.is_default:
                return member
        return None  # If no default is marked, return None or consider raising an error
