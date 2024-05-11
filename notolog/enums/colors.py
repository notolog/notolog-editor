from .enum_base import EnumBase

assert hasattr(EnumBase, 'default'), "Check default() method is implemented in the base class"


class Colors(EnumBase):

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """
        Override _generate_next_value_ to allow for custom attributes on enum members (mostly for default).

        'name' is the name of the Enum's member, which will be 'A', 'B', 'C', etc.
        This method returns the name itself, an 'extended' marker (False), and a 'default' marker (False).

        Extended means extended color palette.
        """
        return name, False, False

    # Red Spectrum
    CRIMSON = ("Crimson", True)
    DARKRED = ("DarkRed", True)
    FIREBRICK = ("Firebrick", True)
    INDIANRED = ("IndianRed", True)
    LIGHTCORAL = ("LightCoral", True)
    MAROON = ("Maroon", False)
    RED = ("Red", False)
    SALMON = ("Salmon", True)
    DARKSALMON = ("DarkSalmon", True)
    TOMATO = ("Tomato", True)

    # Orange Spectrum
    DARKORANGE = ("DarkOrange", True)
    ORANGE = ("Orange", True)
    CORAL = ("Coral", True)
    ORANGERED = ("OrangeRed", True)

    # Yellow Spectrum
    GOLD = ("Gold", True)
    YELLOW = ("Yellow", False)
    LIGHTGOLDENRODYELLOW = ("LightGoldenrodYellow", True)
    PALEGOLDENROD = ("PaleGoldenrod", True)
    GOLDENROD = ("Goldenrod", True)
    DARKGOLDENROD = ("DarkGoldenrod", True)

    # Green Spectrum
    GREENYELLOW = ("GreenYellow", True)
    CHARTREUSE = ("Chartreuse", True)
    LAWNGREEN = ("LawnGreen", True)
    LIME = ("Lime", False)
    LIMEGREEN = ("LimeGreen", True)
    PALEGREEN = ("PaleGreen", True)
    LIGHTGREEN = ("LightGreen", True)
    MEDIUMSPRINGGREEN = ("MediumSpringGreen", True)
    SPRINGGREEN = ("SpringGreen", True)
    MEDIUMSEAGREEN = ("MediumSeaGreen", True)
    SEAGREEN = ("SeaGreen", True)
    FORESTGREEN = ("ForestGreen", True)
    GREEN = ("Green", False)
    DARKGREEN = ("DarkGreen", True)
    YELLOWGREEN = ("YellowGreen", True)
    OLIVEDRAB = ("OliveDrab", True)
    OLIVE = ("Olive", False)

    # Cyan to Blue Spectrum
    MEDIUMAQUAMARINE = ("MediumAquamarine", True)
    AQUAMARINE = ("Aquamarine", True)
    TURQUOISE = ("Turquoise", True)
    MEDIUMTURQUOISE = ("MediumTurquoise", True)
    DARKTURQUOISE = ("DarkTurquoise", True)
    LIGHTSEAGREEN = ("LightSeaGreen", True)
    CADETBLUE = ("CadetBlue", True)
    DARKCYAN = ("DarkCyan", True)
    TEAL = ("Teal", False)
    CYAN = ("Cyan", True)
    LIGHTCYAN = ("LightCyan", True)
    AQUA = ("Aqua", False)
    PALETURQUOISE = ("PaleTurquoise", True)
    AZURE = ("Azure", True)
    ALICEBLUE = ("AliceBlue", True)

    # Blue Spectrum
    NAVY = ("Navy", False)
    DARKBLUE = ("DarkBlue", True)
    MEDIUMBLUE = ("MediumBlue", True)
    BLUE = ("Blue", False)
    MIDNIGHTBLUE = ("MidnightBlue", True)
    ROYALBLUE = ("RoyalBlue", True)
    STEELBLUE = ("SteelBlue", True)
    DODGERBLUE = ("DodgerBlue", True)
    DEEPSKYBLUE = ("DeepSkyBlue", True)
    CORNFLOWERBLUE = ("CornflowerBlue", True)
    SKYBLUE = ("SkyBlue", True)
    LIGHTSKYBLUE = ("LightSkyBlue", True)
    SLATEBLUE = ("SlateBlue", True)
    DARKSLATEBLUE = ("DarkSlateBlue", True)
    MEDIUMSLATEBLUE = ("MediumSlateBlue", True)

    # Violet and Magenta Spectrum
    LAVENDER = ("Lavender", True)
    BLUEVIOLET = ("BlueViolet", True)
    DARKVIOLET = ("DarkViolet", True)
    PURPLE = ("Purple", False)
    MEDIUMPURPLE = ("MediumPurple", True)
    INDIGO = ("Indigo", True)
    DARKORCHID = ("DarkOrchid", True)
    DARKMAGENTA = ("DarkMagenta", True)
    MAGENTA = ("Magenta", True)
    ORCHID = ("Orchid", True)
    VIOLET = ("Violet", True)
    PLUM = ("Plum", True)
    THISTLE = ("Thistle", True)
    LAVENDERBLUSH = ("LavenderBlush", True)
    MEDIUMVIOLETRED = ("MediumVioletRed", True)
    PALEVIOLETRED = ("PaleVioletRed", True)

    # Neutral and Light Spectrum
    GAINSBORO = ("Gainsboro", True)
    LIGHTGREY = ("LightGrey", True)
    SILVER = ("Silver", False)
    DARKGRAY = ("DarkGray", True)
    GRAY = ("Gray", False)
    DIMGRAY = ("DimGray", True)
    LIGHTSLATEGRAY = ("LightSlateGray", True)
    SLATEGRAY = ("SlateGray", True)
    DARKSLATEGRAY = ("DarkSlateGray", True)
    BLACK = ("Black", False, True)
    WHITE = ("White", False)
    SNOW = ("Snow", True)
    HONEYDEW = ("Honeydew", True)
    MINTCREAM = ("MintCream", True)
    GHOSTWHITE = ("GhostWhite", True)
    WHITESMOKE = ("WhiteSmoke", True)
    SEASHELL = ("Seashell", True)
    BEIGE = ("Beige", True)
    OLDLACE = ("OldLace", True)
    FLORALWHITE = ("FloralWhite", True)
    IVORY = ("Ivory", True)
    ANTIQUEWHITE = ("AntiqueWhite", True)
    LINEN = ("Linen", True)
    MISTYROSE = ("MistyRose", True)
    PAPAYAWHIP = ("PapayaWhip", True)
    BLANCHEDALMOND = ("BlanchedAlmond", True)
    BISQUE = ("Bisque", True)
    PEACHPUFF = ("PeachPuff", True)
    NAVAJOWHITE = ("NavajoWhite", True)
    MOCCASIN = ("Moccasin", True)
    CORNSILK = ("CornSilk", True)
    LEMONCHIFFON = ("LemonChiffon", True)
    KHAKI = ("Khaki", True)
    WHEAT = ("Wheat", True)

    def __init__(self, value, is_extended=False, is_default=False):
        # If the value is a tuple, unpack it.
        if isinstance(value, tuple):
            self._value_, self.is_extended, self.is_default = value
        else:
            self._value_ = value
            self.is_extended = is_extended
            self.is_default = is_default

    @classmethod
    def extended_members(cls):
        return [member for member in cls if member.is_extended]

    @classmethod
    def is_extended(cls, member):
        return member in cls.extended_members()
