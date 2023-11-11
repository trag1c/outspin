import sys
import termios
import tty


def _unsafe_getch() -> str:
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def clear_stdin() -> None:
    termios.tcflush(sys.stdin, termios.TCIOFLUSH)


def getch() -> str:
    ch = _unsafe_getch()
    if ch == "\x03":
        raise KeyboardInterrupt
    if ch == "\x04":
        raise EOFError
    return ch
