from notolog.enums.enum_base import EnumBase

assert hasattr(EnumBase, 'default'), "Check default() method is implemented in the base class"


class SomethingEnum(EnumBase):
    """
    Enum for testing 'something' behavior or options.
    """

    SMTH1 = "Smth1"
    SMTH2 = ("Smth2", True)  # Fallback default option
    SMTH3 = "Smth3"
