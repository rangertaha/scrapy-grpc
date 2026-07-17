# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Raised the minimum supported Python to 3.12 per SPEC 0 (supported range
  is now 3.12–3.14): `requires-python = ">=3.12"`, trove classifiers, CI
  matrix, and Ruff/mypy target versions all updated.
- Upgraded dependency floors to the latest stable releases: `Scrapy>=2.17`
  (was `>=2.16`); dev tooling floors raised to `pytest>=9`, `ruff>=0.15`,
  `mypy>=2`.
- Regenerated `uv.lock` for the 3.12+ baseline (drops the `exceptiongroup`
  and `tomli` backports).
- Declared support for Python 3.14.

- Moved the package to the standard `src/` layout (`src/scrapy_grpc/`);
  the import path `scrapy_grpc` is unchanged.
- Modernized packaging to PEP 621 `pyproject.toml` with the `hatchling`
  build backend, and set up PyPI publishing via GitHub Actions with
  Trusted Publishing (OIDC).

### Added

- `uv.lock` lockfile pinning the resolved development environment.
- Type annotations and a `py.typed` marker (PEP 561).
- Test suite (`tests/`) covering the `WebService` extension: settings
  handling, signal-handler registration, and log output (100% line
  coverage of the implemented code, measured with `pytest-cov`).
- CI workflow running Ruff, mypy, and pytest across Python 3.12–3.14.
- Ruff and mypy configuration in `pyproject.toml`, plus a `dev`
  dependency group (including `pytest-cov` for coverage reporting).
- Module docstrings documenting that `scrapy_grpc.client` is a
  placeholder: the gRPC service interface and client are not
  implemented yet.

### Removed

- Unused `grpcio` runtime dependency: nothing in the package imports
  `grpc` yet (the gRPC client is an unimplemented placeholder). It will
  be re-added when the gRPC service and client are implemented.

### Fixed

- Typo in the engine-started log message ("Stat" → "Start").

## [1.0.0] - 2017-09-27

### Added

- Initial release: `WebService` Scrapy extension with `GRPC_ENABLED`,
  `GRPC_HOST`, and `GRPC_PORT` settings.
