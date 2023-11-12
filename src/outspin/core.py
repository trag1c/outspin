from __future__ import annotations

from outspin.utils import getch

MODS = {
    "\x1b[A": "up",
    "\x1b[B": "down",
    "\x1b[C": "right",
    "\x1b[D": "left",
    " ": "space",
    "\t": "tab",
    "\r": "enter",
}


def get_key() -> str:
    return MODS.get(ch := getch(), ch)


def wait_for(*keys: str) -> str:
    while (key := get_key()) not in keys:
        pass
    return key


def pause(prompt: str | None = None) -> None:
    if prompt is None:
        prompt = "Press any key to continue..."
    print(prompt, end="", flush=True)
    getch()
    print()
