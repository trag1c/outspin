from __future__ import annotations

import os
import termios
import tty


class OutspinError(Exception):
    """Base class for exceptions raised by outspin."""


class OutspinValueError(OutspinError, ValueError):
    """Exception for value errors related to outspin's API."""


def _getch() -> str:  # pragma: no cover
    old_state = termios.tcgetattr(1)
    tty.setcbreak(1)
    try:
        return os.read(1, 8).decode("utf-8")
    finally:
        termios.tcsetattr(1, termios.TCSADRAIN, old_state)


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
    "\x0c": "^L",
    "\x04": "^D",
    "\x03": "^C",
}


def get_key() -> str:
    """Return a keypress from standard input."""
    return _MODS.get(ch := _getch(), ch)


def wait_for(*keys: str) -> str:
    """Wait for one of the keys to be pressed and return it."""
    if not keys:
        raise OutspinValueError("No keys to wait for")
    while (key := get_key()) not in keys:
        pass
    return key


def pause(prompt: str | None = None) -> None:
    """Display the prompt and pause the program until a key is pressed."""
    if prompt is None:
        prompt = "Press any key to continue..."
    print(prompt, end="", flush=True)
    _getch()
    print()
