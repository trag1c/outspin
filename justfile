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
    interrogate src/outspin/

# runs pytest, mypy and ruff
check:
    pytest
    mypy src/outspin/
    ruff check src/outspin/
    ruff format src/outspin/ --check
