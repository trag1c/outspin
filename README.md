# outspin

`outspin` is a tiny, low-abstraction library bringing C's `getch()`
functionality to Python, with a sane API. An ideal choice for developers seeking
direct control over their TUI applications.

- [Installation](#installation)
- [Examples](#examples)
  - [Select Menu](#select-menu)
  - [Typing Test](#typing-test)
- [Reference](#reference)
  - [`get_key`](#get_key)
  - [`wait_for`](#wait_for)
  - [`pause`](#pause)
  - [`constants`](#constants)
- [Known Issues](#known-issues)
- [Contributing](#contributing)
- [License](#license)

## Installation

From PyPI:
```bash
pip install outspin
```
From source:
```bash
pip install git+https://github.com/trag1c/outspin.git
```

## Examples

### Select Menu

https://github.com/trag1c/outspin/assets/77130613/ea0be955-302d-4ff3-85c9-8f7c451e6026

<details>
    <summary>Source</summary>

```py
from outspin import wait_for


def _display_selected(*options: str, selected: int) -> None:
    print("Select an option:")
    for i, option in enumerate(options):
        print(f"{'>' if i == selected else ' '} {option}")
    print(f"\033[{len(options) + 1}F", end="")


def select(*options: str) -> str:
    selected = 0
    _display_selected(*options, selected=selected)
    while (key := wait_for("up", "down", "enter")) != "enter":
        selected += 1 if key == "down" else -1
        selected %= len(options)
        _display_selected(*options, selected=selected)
    print("\n" * len(options))
    return options[selected]


print("Selected", select("Python", "Rust", "Swift", "C++", "C", "Kotlin"))
```
</details>

### Typing Test

https://github.com/trag1c/outspin/assets/77130613/c44a8d2f-8b1e-4948-8e78-15018e2e3667

<details>
  <summary>Source</summary>

> Requires [dahlia] and [nouns.txt]
```py
from __future__ import annotations

import sys
from collections.abc import Iterator
from datetime import datetime
from itertools import count, islice, zip_longest
from pathlib import Path
from random import choice
from string import ascii_lowercase

from dahlia import dprint
from outspin import pause, wait_for

NOUNS = [
    w
    for w in Path("nouns.txt").read_text().splitlines()
    if len(w) < 12 and w.isalpha()
]


class WordQueue:
    def __init__(self) -> None:
        self._gen = (choice(NOUNS) for _ in count())
        self._queue: list[str] = []
        self.load(4)

    def load(self, number: int = 1) -> None:
        self._queue.extend(islice(self._gen, number))

    @property
    def loaded(self) -> tuple[str, ...]:
        return tuple(self._queue)

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        self._queue.pop(0)
        self.load()
        return self._queue[0]


def render(wq: WordQueue, buffer: list[str]) -> None:
    current, *up_next = wq.loaded
    buf_str = "".join(buffer)
    first_bad_idx = (
        (
            next(
                i
                for i, (a, b) in enumerate(zip_longest(buf_str, current, fillvalue="_"))
                if a != b
            )
            if buf_str != current
            else len(current)
        )
        if buf_str and current
        else 0
    )
    dprint(f"\033[2F\033[0JUp next: &2{' '.join(up_next)}")
    print(f"\n> {buf_str[:first_bad_idx]}", end="")
    if bad_content := buf_str[first_bad_idx:]:
        dprint(f"&4{bad_content}&8{current[first_bad_idx+len(bad_content):]}", end="")
    else:
        dprint(f"&8{current[first_bad_idx:]}", end="")
    sys.stdout.flush()


def main(time: int) -> None:
    pause()
    start_time = datetime.now()

    wq = WordQueue()
    buffer: list[str] = []
    word = list(next(wq))
    typed_chars = 0

    while (datetime.now() - start_time).seconds < time:
        render(wq, buffer)
        key = wait_for(*ascii_lowercase, "space", "backspace")
        if key == "space":
            if buffer == word:
                buffer = []
                typed_chars += len(word) + 1
                word = list(next(wq))
        elif key == "backspace":
            if buffer:
                buffer.pop()
        else:
            buffer.append(key)

    print(f"\nWPM: {(typed_chars - 1) / 5 / (time / 60):.2f}")


if __name__ == "__main__":
    main(int(sys.argv[1] if len(sys.argv) > 1 else 30))
```
</details>

## Reference

### `get_key`
> Signature: `() -> None`

Returns a keypress from standard input. It exclusively identifies keypresses
that result in tangible inputs, therefore modifier keys like `shift` or
`caps lock` are ignored. `outspin` also returns the actual input, meaning that
pressing, for instance, `shift+a` will make `get_key()` return `A`.

> [!Note]
> `outspin` translates dozens of ANSI codes to human-readable names under the
> hood. If you spot a case where an ANSI code (e.g. `\x1b[15;2~`) doesn't get
> converted, please open an issue and/or submit a PR adding the code.

### `wait_for`
> Signature: `(*keys: str) -> str`

Waits for one of the keys to be pressed and returns it.
```pycon
>>> wait_for(*"wasd")  # pressing g t 4 2 q a
'a'
```
`wait_for` requires at least one key to be provided.
```pycon
>>> wait_for()
outspin.OutspinValueError: No keys to wait for
```

### `pause`
> Signature: `(prompt: str | None = None) -> None`

Displays the prompt and pauses the program until a key is pressed.  
The default prompt is `Press any key to continue...`.

### `constants`

A namespace containing a few useful characters groups:
- `ARROWS`: `up` `down` `left` `right`
- `F_KEYS`: `f1` → `f12`
- `DIGITS` or `NUMBERS`: `0` → `9` (same as `string.digits`)
- `LOWERCASE`: `a` → `z` (same as `string.ascii_lowercase`)
- `UPPERCASE`: `A` → `Z` (same as `string.ascii_uppercase`)
- `LETTERS`: `LOWERCASE` + `UPPERCASE` (same as `string.ascii_letters`)
- `PUNCTUATION`: ``!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~`` (same as
  `string.punctuation`)

## Known Issues
* Some combinations (like `shift+up` or `alt+shift+right`) may not work
  correctly on Windows.

## Contributing

Contributions are welcome! 

Please open an issue before submitting a pull request
(doesn't apply to minor changes like typos).

To get started:

1. Clone the project:
```bash
git clone https://github.com/trag1c/outspin.git
```

2. Set up the project with [just] (make sure you have [poetry] installed):
```bash
just install
```

> [!Note]
> If you don't want to install `just`, simply look up the recipes
> in the project's `justfile`.

3. After you're done, use the following `just` recipes to check your changes:
```bash
just check     # pytest, mypy, ruff 
just coverage  # pytest (with coverage), interrogate (docstring coverage)
```

## License
`outspin` is licensed under the [MIT License].  
© [trag1c], 2023–2024

[MIT License]: https://opensource.org/license/mit/
[poetry]: https://python-poetry.org/
[just]: https://github.com/casey/just/
[trag1c]: https://github.com/trag1c/
[dahlia]: https://github.com/dahlia-lib/dahlia/
[nouns.txt]: https://gist.github.com/trag1c/f74b2ab3589bc4ce5706f934616f6195/