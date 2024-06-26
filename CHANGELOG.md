# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.3.2] - 2024-04-29

### Fixed
- (Unix) `get_key()` now returns `^C` instead of raising `KeyboardInterrupt`,
  making it consistent with the Windows implementation

## [v0.3.1] - 2024-04-19

### Added
- Handling `ctrl` + arrows on Unix ([#4] + [#5] by [@qexat])
- `wait_for` now has a `() -> Never` overload
- `py.typed` marker file
- Defined an `__all__` containing:
  - the `get_key`, `pause`, and `wait_for` functions
  - the `OutspinError`, `OutspinImportError`, and `OutspinValueError` exceptions

### Fixed
- Windows' `get_key()` implementation will no longer raise an exception when it
  fails to decode an unmapped keypress

[#4]: https://github.com/trag1c/outspin/pull/4
[#5]: https://github.com/trag1c/outspin/pull/5
[@qexat]: https://github.com/qexat

## [v0.3.0] - 2024-01-28

### Added
- Windows support

## [v0.2.0] - 2023-11-27

### Added
- [`constants`](https://github.com/trag1c/outspin#constants) namespace
- `backspace` and `delete` are now correctly recognized
- Various modifier key combos are now recognized:
  - `shift` + `tab`
  - `shift` + `alt` + arrows
  - `shift` + `ctrl` + arrows
  - `shift` + function keys
  - `ctrl` + A, B, E..H, K, N..Z

### Changed
- `outspin` now explicitly throws an OSError when attempted to be imported on
  Windows

### Fixed
- `wait_for` no longer hangs when called with no arguments


## [v0.1.0] - 2023-11-19

Initial release 🎉


[v0.1.0]: https://github.com/trag1c/outspin/releases/tag/v0.1.0
[v0.2.0]: https://github.com/trag1c/outspin/compare/v0.1.0...v0.2.0
[v0.3.0]: https://github.com/trag1c/outspin/compare/v0.2.0...v0.3.0
[v0.3.1]: https://github.com/trag1c/outspin/compare/v0.3.0...v0.3.1
[v0.3.2]: https://github.com/trag1c/outspin/compare/v0.3.1...v0.3.2
