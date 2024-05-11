class EncPassword:
    """
    Password object class to store password related data.
    """

    def __init__(self):
        self._password = None
        self._hint = None

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def hint(self):
        return self._hint

    @hint.setter
    def hint(self, value):
        self._hint = value

    def is_valid(self):
        if self._password is None:
            return False
        if len(self._password) < 8:
            return False
        return True
