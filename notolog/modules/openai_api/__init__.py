from .module_core import ModuleCore


def get_name():
    """
    Readable module name.
    """
    return ModuleCore.module_name


def is_available() -> bool:
    """
    No additional requirements.
    """
    return True
