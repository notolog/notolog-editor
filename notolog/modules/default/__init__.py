from .module_core import ModuleCore


def get_name():
    """
    Readable module name, for example, 'Default Module'.
    """
    return ModuleCore.module_name


def is_available() -> bool:
    """
    Check for any additional requirements for the module here.
    """
    return True
