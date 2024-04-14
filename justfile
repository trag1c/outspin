[private]
default:
    @just --list

# creates and activate a Poetry environment
install:
    poetry install
    poetry shell

# checks test and docstring coverage
coverage:
    pytest --cov=outspin --cov-report term-missing
    interrogate

# runs pytest, mypy and ruff
check:
    pytest
    mypy --strict outspin tests
    ruff check
    ruff format --check
