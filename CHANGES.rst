Change Log
==========
0.4.4 (2022-12-03)
------------------
Unreleased

- Created new Forecasts feature which returns an interable MeteorologicalPredictions object filled with MeteorologicalPrediction objects which has forecast data

0.4.3 (2022-09-19)
------------------

Documentation
~~~~~~~~~~~~~

- Scaffold and publish documentation.

Internal
~~~~~~~~

- Update all dependencies to latest.
- Organize dependencies in ``pyproject.toml`` by groups (e.g., "dev" and "docs").

0.4.2 (2022-09-05)
------------------

mypy
~~~~

- **Types**: ``realtime.get`` `infers exact return type`_ from user-provided value for ``dataset``.

ObservationDatum
~~~~~~~~~~~~~~~~

Refers to a particular piece of data from an ``Observation``. Metadata can be accessed
with ``.label``, ``.unit``, and ``.value`` (e.g., ``wind_direction.value``).

- **ObservationFloatDatum**: validate numeric values (previously ``ObservationDatum``).
- **ObservationStringDatum**: validate non-numeric values.

Observation
~~~~~~~~~~~

Weather observation recorded at unique datetime by type of ``dataset`` (e.g., meteorological).

- **MeteorologicalObservation**: attributes return either ``ObservationFloatDatum``
  or `ObservationStringDatum` after validating data provided from NDBC.
- **WaveSummaryObservation**: attributes return either ``ObservationFloatDatum``
  or ``ObservationStringDatum`` after validating data provided from NDBC.

Observations
~~~~~~~~~~~~

The following models were extended from ``Observations`` to support static typing:

- **MeteorologicalObservations**: can use ``+=`` syntax on an instance
  of this class in order to append ``MeteorologicalObservation`` records.
- **WaveSummaryObservations**: can use ``+=`` syntax on an instance
  of this class in order to append ``WaveSummaryObservation`` records.

Internal
~~~~~~~~

- Bump all development dependencies to latest.
- Extend tests to check for expected attributes.

0.4.1 (2022-08-31)
------------------

Observation
~~~~~~~~~~~

- **MeteorologicalObservation**: change ``dominate_wave_period`` to
  ``dominant_wave_period``.

0.4.0 (2022-08-29)
------------------

Buoy
~~~~

- **Realtime**: ``get`` now supports Wave Summary data (i.e., dataset="spec").

Observation
~~~~~~~~~~~

- **MeteorologicalObservation**: new model of type ``Observation``
  to represent API calls for realtime meteorological data. Attributes
  return instances of ``ObservationDatum`` by label (snaked cased).
  This directly supports enhancements for static type checking introduced
  in this release.

- **WaveSummaryObservation**: new model of type ``Observation`` to
  represent API calls for realtime wave summary data. Attributes
  return instances of ``ObservationDatum`` by label (snaked cased).
  This directly supports enhancements for static type checking
  introduced in this release.

- **ObservationDatum**: renamed ``Observation`` to ``ObservationDatum``.
  This represents a piece of data that was observed by a buoy at a unique
  datetime and contains metadata like unit of measurement (i.e., ``.unit``).
  It is renamed to better define its function and purpose.

mypy
~~~~

- **Types**: extend type checking support to all objects and iterables.

Internal
~~~~~~~~

- Update tests to account for incoming changes.
- Bump all dependencies to latest.

Breaking Changes
-------------------

Observations
~~~~~~~~~~~~

- **Observation**: is now ``ObservationDatum``; the original purpose of
  ``Observation``, which was introduced in v0.3.0, has been moved to
  this new object.

- **ObservationDatum**: value will default to ``None`` (type: NoneType)
  when datum missing instead of ``nan`` (type: float). This change should
  improve experience when working with ``JSON`` objects or databases.

- **Observations**: container for models of type ``Observation`` such as
  ``MeteorologicalObservation``, which will be new response type for all
  API calls.

Buoy
~~~~

- **Realtime**: ``get`` returns an iterable ``Observations`` object. The type of
  iterable provided depends on the query. If requesting meteorological data, type
  of ``Observation`` would be ``MeteorologicalObservation``. The primary purpose
  of these types of ``Observation`` objects is to define available attributes.

0.3.0 (2022-08-12)
------------------

Buoy
~~~~

- **Realtime**: ``get`` returns list of ``Observation`` instances. Instance
  of ``Observation`` will default to ``nan`` (type: float) when datum is missing.

mypy
~~~~

- **Types**: provide type annotations to support static type checking.

Internal
~~~~~~~~

- Add new ``pre-commit`` hooks and update all other hooks to latest version.
- Address PEP8 warnings identified by flake8.
- Refactor all imports to absolute from relative.
- Bump all dependencies to latest.

Documentation
~~~~~~~~~~~~~

- Fix broken href in CONTRIBUTING.
- Update `doc/examples`_ with examples of query response.

0.2.0 (2022-07-10)
------------------

Buoy
~~~~

- **Realtime**: ``get`` returns ``None`` when data cannot be successfully retrieved.

Documentation
~~~~~~~~~~~~~

- Update documentation and examples with revised syntax.

Breaking Changes
----------------

Buoy
~~~~

- **Realtime**: ``Buoy`` class instantiation no longer accepts arguments.
  - ``station_id`` must now be provided as an argument for every request (see examples in docs).

0.1.1 (2022-07-04)
------------------

Documentation
~~~~~~~~~~~~~

- Add examples and installation instructions.

0.1.0 (2022-07-04)
------------------

🎉 **Initial release** 🎉

Features
~~~~~~~~

- Get realtime data for buoy by ``station_id``.
  - encapsulates realtime data with ``Observation`` class.
- Get list of all active stations.

Internal
~~~~~~~~

- Incorporate githooks with ``pre-commit`` for development workflow.

.. _doc/examples: https://github.com/clairBuoyant/pybuoy/tree/main/docs/examples
..  _infers exact return type: https://github.com/clairBuoyant/pybuoy/pull/14#issue-1362358830
