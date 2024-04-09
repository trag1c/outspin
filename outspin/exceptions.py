class OutspinError(Exception):
    """Base class for exceptions raised by outspin."""


class OutspinValueError(OutspinError, ValueError):
    """Exception for value errors related to outspin's API."""


class OutspinImportError(OutspinError, ImportError):
    """Exception for import errors related to outspin's API."""
