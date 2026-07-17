# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Implemented the gRPC service: the `WebService` extension now starts a
  gRPC server (`grpcio`) when the crawler engine starts and stops it when
  the engine stops. The `Crawler` service (defined in
  `src/scrapy_grpc/pb/scrapy_grpc.proto`) exposes `GetStatus` (spider
  name, running state, items scraped), `GetStats` (stats collector
  snapshot), and `StopCrawler` (graceful shutdown via the Twisted
  reactor).
- `scrapy_grpc.CrawlerClient`: a blocking Python client for the service,
  usable as a context manager, re-exported with `WebService` from the
  package root.
- Runtime dependencies on `grpcio` and `protobuf`; dev dependency on
  `grpcio-tools` for regenerating the stubs.
- Test suite (`tests/`) covering settings handling, signal-handler
  registration, and an end-to-end round trip exercising the client
  against a live in-process server.
- `uv.lock` lockfile pinning the resolved development environment.
- Type annotations and a `py.typed` marker (PEP 561).
- CI workflow running Ruff, mypy, and pytest across Python 3.12–3.14.
- Ruff and mypy configuration in `pyproject.toml`, plus a `dev`
  dependency group (including `pytest-cov` for coverage reporting).

### Changed

- **Breaking:** raised the minimum supported Python to 3.12 per SPEC 0
  (supported range is now 3.12–3.14): `requires-python = ">=3.12"`,
  trove classifiers, CI matrix, and Ruff/mypy target versions all
  updated. Declared support for Python 3.14.
- `GRPC_PORT` is now read with `settings.getint()` (string values from
  the CLI/environment work), and setting it to `0` binds a free ephemeral
  port, with `WebService.port` updated to the bound port.
- `item_scraped` now counts scraped items (surfaced via `GetStatus`)
  instead of logging each item at INFO level.
- Upgraded dependency floors to the latest stable releases: `Scrapy>=2.17`
  (was `>=2.16`); dev tooling floors raised to `pytest>=9`, `ruff>=0.15`,
  `mypy>=2`.
- Moved the package to the standard `src/` layout (`src/scrapy_grpc/`);
  the import path `scrapy_grpc` is unchanged.
- Modernized packaging to PEP 621 `pyproject.toml` with the `hatchling`
  build backend, and set up PyPI publishing via GitHub Actions with
  Trusted Publishing (OIDC).

### Fixed

- Typo in the engine-started log message ("Stat" → "Start").

## [1.0.0] - 2017-09-27

### Added

- Initial release: `WebService` Scrapy extension with `GRPC_ENABLED`,
  `GRPC_HOST`, and `GRPC_PORT` settings.
