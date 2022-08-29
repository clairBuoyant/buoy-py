## 0.4.0 (2022-08-29)

### Buoy

- **Realtime**: `get` now supports Wave Summary data (i.e., dataset="spec").

### Observation

- **MeteorologicalObservation**: new model of type `Observation` to represent API calls for realtime meteorological data. Attributes return instances of `ObservationDatum` by label (snaked cased). This directly supports enhancements for static type checking introduced in this release.

- **ObservationDatum**: renamed `Observation` to `ObservationDatum`. This represents a piece of data that was observed by a buoy at a unique datetime and contains metadata like unit of measurement (i.e., `.unit`). It is renamed to better define its function and purpose.

### mypy

- **Types**: extend type checking support to all objects and iterables.

### Internal

- Update tests to account for incoming changes.
- Bump all dependencies to latest.

## Breaking Changes

### Observations

- **Observation**: is now `ObservationDatum`; the original purpose of `Observation`, which was introduced in v0.3.0, has been moved to this new object.

- **ObservationDatum**: value will default to `None` (type: NoneType) when datum missing instead of `nan` (type: float). This change should improve experience when working with `JSON` objects or databases.

- **Observations**: container for models of type `Observation` such as `MeteorologicalObservation`, which will be new response type for all API calls.

### Buoy

- **Realtime**: `get` returns an iterable `Observations` object. The type of iterable provided depends on the query. If requesting meteorological data (e.g., dataset="txt"), type of `Observation` would be `MeteorologicalObservation`. The primary purpose of these types of `Observation` objects is to define available attributes (e.g., "wind_speed").

## 0.3.0 (2022-08-12)

### Buoy

- **Realtime**: `get` returns list of `Observation` instances. Instance of `Observation` will default to `nan` (type: float) when datum is missing.

### mypy

- **Types**: provide type annotations to support static type checking.

### Internal

- Add new `pre-commit` hooks and update all other hooks to latest version.
- Address PEP8 warnings identified by flake8.
- Refactor all imports to absolute from relative.
- Bump all dependencies to latest.

### Documentation

- Fix broken href in [Contributing](./docs/CONTRIBUTING.md#guidelines) guide.
- Update [doc/examples](./docs/examples/) with examples of query response.

## 0.2.0 (2022-07-10)

### Buoy

- **Realtime**: `get` returns `None` when data cannot be successfully retrieved.

### Documentation

- Update documentation and examples with revised syntax.

## Breaking Changes

### Buoy

- **Realtime**: `Buoy` class instantiation no longer accepts arguments.
  - `station_id` must now be provided as an argument for every request (see examples in docs).

## 0.1.1 (2022-07-04)

### Documentation

- Add examples and installation instructions.

## 0.1.0 (2022-07-04)

🎉 **Initial release** 🎉

## Features

- Get realtime data for buoy by `station_id`.
  - encapsulates realtime data with `Observation` class.
- Get list of all active stations.

## Internal

- Incorporate githooks with `pre-commit` for development workflow.
