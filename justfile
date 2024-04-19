[private]
default:
    @just --list

file_to_omit := if os_family() == "windows" { "unix" } else { "windows" }

# creates and activate a Poetry environment
install:
    poetry install
    poetry shell

# checks test and docstring coverage
coverage:
    coverage run --omit=outspin/{{file_to_omit}}.py -m pytest
    coverage report -m
    interrogate

# runs pytest, mypy and ruff
check:
    pytest
    mypy --strict outspin tests
    ruff check
    ruff format --check
