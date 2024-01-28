import sys

if sys.platform in ("win32", "cygwin"):
    from outspin.exceptions import OutspinImportError

    msg = "This module is only available on Unix-like systems."
    raise OutspinImportError(msg)

import os
import termios
import tty
from string import ascii_uppercase

_MODS = {
    "\x1b": "esc",
    "\x7f": "backspace",
    "\x1b[3~": "delete",
    "\x1b[A": "up",
    "\x1b[B": "down",
    "\x1b[C": "right",
    "\x1b[D": "left",
    " ": "space",
    "\t": "tab",
    "\x1b[Z": "shift+tab",
    "\r": "enter",
    "\n": "enter",
    "\r\n": "enter",
    "\x1bOP": "f1",
    "\x1bOQ": "f2",
    "\x1bOR": "f3",
    "\x1bOS": "f4",
    "\x1b[15~": "f5",
    "\x1b[17~": "f6",
    "\x1b[18~": "f7",
    "\x1b[19~": "f8",
    "\x1b[20~": "f9",
    "\x1b[21~": "f10",
    "\x1b[23~": "f11",
    "\x1b[24~": "f12",
    "\x1b[1;2A": "shift+up",
    "\x1b[1;2B": "shift+down",
    "\x1b[1;2C": "shift+right",
    "\x1b[1;2D": "shift+left",
    "\x1b\x1b[A": "alt+up",
    "\x1b\x1b[B": "alt+down",
    "\x1b\x1b[C": "alt+right",
    "\x1b\x1b[D": "alt+left",
    "\x1b[1;4A": "shift+alt+up",
    "\x1b[1;4B": "shift+alt+down",
    "\x1b[1;4C": "shift+alt+right",
    "\x1b[1;4D": "shift+alt+left",
    "\x1b[1;10A": "shift+alt+up",
    "\x1b[1;10B": "shift+alt+down",
    "\x1b[1;10C": "shift+alt+right",
    "\x1b[1;10D": "shift+alt+left",
    "\x1b[1;6A": "shift+ctrl+up",
    "\x1b[1;6B": "shift+ctrl+down",
    "\x1b[1;6C": "shift+ctrl+right",
    "\x1b[1;6D": "shift+ctrl+left",
    "\x1b[1;2P": "shift+f1",
    "\x1b[1;2Q": "shift+f2",
    "\x1b[1;2R": "shift+f3",
    "\x1b[1;2S": "shift+f4",
    "\x1b[15;2~": "shift+f5",
    "\x1b[17;2~": "shift+f6",
    "\x1b[18;2~": "shift+f7",
    "\x1b[19;2~": "shift+f8",
    "\x1b[20;2~": "shift+f9",
    "\x1b[21;2~": "shift+f10",
    "\x1b[23;2~": "shift+f11",
    "\x1b[24;2~": "shift+f12",
    **{chr(i): f"^{c}" for i, c in enumerate(ascii_uppercase, 1) if c not in "IJM"},
}


def _getch() -> str:  # pragma: no cover
    old_state = termios.tcgetattr(1)
    tty.setcbreak(1)
    try:
        return os.read(1, 8).decode("utf-8")
    finally:
        termios.tcsetattr(1, termios.TCSADRAIN, old_state)


def get_key() -> str:
    """Return a keypress from standard input."""
    return _MODS.get(ch := _getch(), ch)
