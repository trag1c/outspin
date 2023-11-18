from unittest.mock import patch

import pytest

from outspin import get_key, wait_for, pause, OutspinValueError


@pytest.mark.parametrize(
    ("getch_payload", "key"),
    (
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
@patch("outspin._getch")
def test_get_key(getch_mock, getch_payload, key):
    getch_mock.side_effect = None
    getch_mock.return_value = getch_payload
    assert get_key() == key


def test_wait_for_no_keys():
    with pytest.raises(OutspinValueError, match="No keys to wait for"):
        wait_for()


@pytest.mark.parametrize(
    ("wait_for_keys", "pressed_keys", "returned_key"),
    (
        (tuple("wasd"), ("q", "w"), "w"),
        (("f7", "f8"), ("f6", "f9", "f8"), "f8"),
        (("up",), ("down", "left", "right", "up"), "up"),
    ),
)
@patch("outspin.get_key")
def test_wait_for(get_key_mock, wait_for_keys, pressed_keys, returned_key):
    get_key_mock.side_effect = pressed_keys
    assert wait_for(*wait_for_keys) == returned_key


@pytest.mark.parametrize(
    "prompt",
    (
        None,
        "Press any key!",
    ),
)
@patch("outspin._getch")
def test_pause(getch_mock, prompt):
    getch_mock.return_value = "x"
    with patch("builtins.print") as print_mock:
        pause(prompt)
        pause_prompt = "Press any key to continue..." if prompt is None else prompt
        calls = print_mock.call_args_list
        assert calls[0].args[0] == pause_prompt
        assert calls[1].args == ()
