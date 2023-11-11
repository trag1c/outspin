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


class Buffer:
    def __init__(self) -> None:
        self._buffer = ""

    def write(self, value: str) -> None:
        self._buffer += value

    def flush(self) -> str:
        buffer = self._buffer
        self._buffer = ""
        return MODS.get(buffer, buffer)

    def __len__(self) -> int:
        return len(self._buffer)

    def __bool__(self) -> bool:
        return bool(self._buffer)


buffer = Buffer()


def get_key() -> str:
    ch = getch()
    if ch == "\x1b":
        buffer.write(ch)
        buffer.write(getch())
        buffer.write(getch())
    if len(buffer) == 3:
        return buffer.flush()
    return MODS.get(ch, ch)


def wait_for(*keys: str) -> None:
    while get_key() not in keys:
        pass


def pause(prompt: str | None = None) -> None:
    if prompt is None:
        prompt = "Press any key to continue..."
    print(prompt, end="", flush=True)
    getch()
    print()
