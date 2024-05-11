from .enum_base import EnumBase

assert hasattr(EnumBase, 'default'), "Check default() method is implemented in the base class"


class Themes(EnumBase):

    DEFAULT = ("Default", True)  # The second item in the tuple marks this as the default
    CALLIGRAPHY = "Calligraphy"
    NOIR_DARK = "Noir Dark"
    STRAWBERRY = "Strawberry"

    def __init__(self, value, is_default=False):
        self._value_ = value
        self.is_default = is_default
