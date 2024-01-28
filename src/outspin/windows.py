import sys

if sys.platform not in ("win32", "cygwin"):
    from outspin.exceptions import OutspinImportError

    msg = "This module is only available on Windows."
    raise OutspinImportError(msg)

import msvcrt
from string import ascii_uppercase

_MODS = {
    b"\x1b": "esc",
    b"\x08": "backspace",
    b"\xe0S": "delete",
    b"\xe0H": "up",
    b"\xe0P": "down",
    b"\xe0M": "right",
    b"\xe0K": "left",
    b" ": "space",
    b"\t": "tab",
    b"\r": "enter",
    b"\n": "enter",
    b"\rn": "enter",
    b"\x00;": "f1",
    b"\x00<": "f2",
    b"\x00=": "f3",
    b"\x00>": "f4",
    b"\x00?": "f5",
    b"\x00@": "f6",
    b"\x00A": "f7",
    b"\x00B": "f8",
    b"\x00C": "f9",
    b"\x00D": "f10",
    b"\x00\x85": "f11",
    b"\xe0\x86": "f12",
    b"\x00\x98": "alt+up",
    b"\x00\xa0": "alt+down",
    b"\x00\x9d": "alt+right",
    b"\x00\x9b": "alt+left",
    b"\xe0\x8d": "ctrl+up",
    b"\xe0\x91": "ctrl+down",
    b"\xe0t": "ctrl+right",
    b"\xe0s": "ctrl+left",
    b"\x00T": "shift+f1",
    b"\x00U": "shift+f2",
    b"\x00V": "shift+f3",
    b"\x00W": "shift+f4",
    b"\x00X": "shift+f5",
    b"\x00Y": "shift+f6",
    b"\x00Z": "shift+f7",
    b"\x00[": "shift+f8",
    b"\x00\\": "shift+f9",
    b"\x00]": "shift+f10",
    b"\xe0\x87": "shift+f11",
    b"\xe0\x88": "shift+f12",
    **{
        chr(i).encode(): f"^{c}"
        for i, c in enumerate(ascii_uppercase, 1)
        if c not in "IJM"
    },
}


def _getch() -> bytes:  # pragma: no cover
    ks = msvcrt.getch()
    if ks in b"\x00\xe0":
        ks += msvcrt.getch()
    return ks


def get_key() -> str:
    """Return a keypress from standard input."""
    return _MODS.get(ch := _getch(), ch.decode("cp1252"))
