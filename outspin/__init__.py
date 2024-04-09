from __future__ import annotations

import sys
from typing import TYPE_CHECKING, overload

from outspin.exceptions import OutspinError, OutspinImportError, OutspinValueError

if TYPE_CHECKING:
    from typing_extensions import Never

if sys.platform == "win32" or sys.platform == "cygwin":
    from outspin.windows import _getch, get_key
else:
    from outspin.unix import _getch, get_key

__all__ = (
    "OutspinError",
    "OutspinImportError",
    "OutspinValueError",
    "get_key",
    "pause",
    "wait_for",
)


@overload
def wait_for() -> Never: ...


@overload
def wait_for(*keys: str) -> str: ...


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
