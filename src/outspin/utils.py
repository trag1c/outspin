import os
import termios
import tty


def getch() -> str:
    old_state = termios.tcgetattr(1)
    tty.setcbreak(1)
    try:
        return os.read(1, 8).decode("utf-8")
    finally:
        termios.tcsetattr(1, termios.TCSADRAIN, old_state)
