from .enum_base import EnumBase

assert hasattr(EnumBase, 'default'), "Check default() method is implemented in the base class"


class AiModelNames(EnumBase):

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Override _generate_next_value_ to allow for custom attributes on enum members (mostly for default).

        'name' is the name of the Enum's member, which will be 'A', 'B', 'C', etc.
        This method returns the name itself, a 'legacy' marker (False), and a 'default' marker (False)

        Legacy means the outdated model, e.g. legacy completions that is still supported.
        """
        return name, False, False

    GPT_3_5 = ("gpt-3.5-turbo", False, True)  # The third item in the tuple marks this as the default
    GPT_3_5_LEGACY = ("gpt-3.5-turbo-instruct", True)  # Second param is a legacy flag (e.g. legacy completions)

    def __init__(self, value, legacy=False, is_default=False):
        # If the value is a tuple, unpack it.
        if isinstance(value, tuple):
            self._value_, self.legacy, self.is_default = value
        else:
            self._value_ = value
            self.legacy = legacy
            self.is_default = is_default

    @classmethod
    def legacy_members(cls):
        return [member for member in cls if member.legacy]

    @classmethod
    def legacy(cls, member):
        return member in cls.legacy_members()
