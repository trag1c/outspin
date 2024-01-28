from __future__ import annotations

from outspin.exceptions import OutspinValueError

try:
    from outspin.unix import _getch, get_key
except ImportError:
    from outspin.windows import _getch, get_key


def wait_for(*keys: str) -> str:
    """Wait for one of the keys to be pressed and return it."""
    if not keys:
        msg = "No keys to wait for"
        raise OutspinValueError(msg)
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
