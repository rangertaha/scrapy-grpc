# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Upgraded dependency floors to the latest stable releases: `Scrapy>=2.17`
  (was `>=2.16`) and `grpcio>=1.82` (was `>=1.81`).
- Declared support for Python 3.14 (supported range is now 3.10–3.14,
  matching Scrapy's own support window).

- Moved the package to the standard `src/` layout (`src/scrapy_grpc/`);
  the import path `scrapy_grpc` is unchanged.
- Modernized packaging to PEP 621 `pyproject.toml` with the `hatchling`
  build backend, and set up PyPI publishing via GitHub Actions with
  Trusted Publishing (OIDC).

### Added

- `uv.lock` lockfile pinning the resolved development environment.
- Type annotations and a `py.typed` marker (PEP 561).
- Test suite (`tests/`) covering the `WebService` extension settings.
- CI workflow running Ruff, mypy, and pytest across Python 3.10–3.14.
- Ruff and mypy configuration in `pyproject.toml`, plus a `dev`
  dependency group.

### Fixed

- Typo in the engine-started log message ("Stat" → "Start").

## [1.0.0] - 2017-09-27

### Added

- Initial release: `WebService` Scrapy extension with `GRPC_ENABLED`,
  `GRPC_HOST`, and `GRPC_PORT` settings.
