[private]
default:
    @just --list

# creates and activate a Poetry environment
install:
    poetry install
    poetry shell

# checks test and docstring coverage
coverage:
    coverage run -m pytest
    coverage report -m
    interrogate

# runs pytest, mypy and ruff
check:
    pytest
    mypy --strict outspin
    mypy tests
    ruff check
    ruff format --check
