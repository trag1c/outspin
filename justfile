[private]
default:
    @just --list

file_to_omit := if os_family() == "windows" { "unix" } else { "windows" }

# checks test and docstring coverage
coverage:
    uv run coverage run --omit=src/outspin/{{file_to_omit}}.py -m pytest
    uv run coverage report -m
    uv run interrogate

# runs pytest, mypy and ruff
check:
    uv run pytest
    uv run mypy --strict src tests
    uv run ruff check
    uv run ruff format --check
