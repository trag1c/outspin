from __future__ import annotations

import sys
from unittest.mock import Mock, patch

import pytest

from outspin import (
    OutspinValueError,
    constants,  # noqa: F401
    get_key,
    pause,
    wait_for,
)

IS_WINDOWS = sys.platform in ("win32", "cygwin")
PLATFORM = "windows" if IS_WINDOWS else "unix"


@pytest.mark.parametrize(
    ("getch_payload", "key"),
    (
        (b"x", "x"),
        (b"\x00?", "f5"),
        (b"\xe0\x87", "shift+f11"),
        (b"\xe0H", "up"),
        (b"\x00\xa0", "alt+down"),
        (b"\x0c", "^L"),
        (b"\x04", "^D"),
        (b"\x03", "^C"),
        (b"\x1b[1;5D", "ctrl+left"),
    )
    if IS_WINDOWS
    else (
        ("x", "x"),
        ("\x1b[15~", "f5"),
        ("\x1b[1;2A", "shift+up"),
        ("\x1b\x1b[B", "alt+down"),
        ("\x1b[1;4D", "shift+alt+left"),
        ("\x0c", "^L"),
        ("\x04", "^D"),
        ("\x03", "^C"),
    ),
)
@patch(f"outspin.{PLATFORM}._getch")
def test_get_key(getch_mock: Mock, getch_payload: bytes, key: str) -> None:
    getch_mock.side_effect = None
    getch_mock.return_value = getch_payload
    assert get_key() == key


def test_wait_for_no_keys() -> None:
    with pytest.raises(OutspinValueError, match="No keys to wait for"):
        wait_for()


@pytest.mark.parametrize(
    ("wait_for_keys", "pressed_keys", "returned_key"),
    [
        (tuple("wasd"), ("q", "w"), "w"),
        (("f7", "f8"), ("f6", "f9", "f8"), "f8"),
        (("up",), ("down", "left", "right", "up"), "up"),
    ],
)
@patch("outspin.get_key")
def test_wait_for(
    get_key_mock: Mock,
    wait_for_keys: tuple[str, ...],
    pressed_keys: tuple[str, ...],
    returned_key: str,
) -> None:
    get_key_mock.side_effect = pressed_keys
    assert wait_for(*wait_for_keys) == returned_key


@pytest.mark.parametrize(
    "prompt",
    [
        None,
        "Press any key!",
    ],
)
@patch("outspin._getch")
def test_pause(getch_mock: Mock, prompt: str | None) -> None:
    getch_mock.return_value = "x"
    with patch("builtins.print") as print_mock:
        pause(prompt)
        pause_prompt = "Press any key to continue..." if prompt is None else prompt
        calls = print_mock.call_args_list
        assert calls[0].args[0] == pause_prompt
        assert calls[1].args == ()
