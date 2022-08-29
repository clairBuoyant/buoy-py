from datetime import datetime

from pybuoy.observation.observation_datum import (
    ObservationFloatDatum,
    ObservationStringDatum,
)
from pybuoy.unit_mappings import (
    METEOROLOGICAL,
    WAVE_SUMMARY,
    MeteorologicalKey,
    WaveSummaryKey,
)

# TODO: support dynamic typing and add slots for efficiency


class BaseObservation:
    """BaseObservation class for `Buoy` readings by datetime."""

    def __init__(self, datetime: datetime = None):
        """Initialize BaseObservation record with datetime.

        Args:
            datetime (datetime): UTC time of value. Defaults to None.
        """
        self._datetime = datetime

    @property
    def datetime(self) -> datetime | None:
        """Return when this observation was made."""
        return self._datetime

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join("{}={!r}".format(k, v) for k, v in self.__dict__.items()),
        )

    def __str__(self):
        return f"Observation({self.datetime})"


class MeteorologicalObservation(BaseObservation):
    """Encapsulates `Buoy` meteorological data."""

    def __init__(
        self,
        values: dict[MeteorologicalKey, str],
        datetime: datetime = None,
    ):
        """Initialize Observation record with relevant metadata.

        Args:
            values (dict[str,str]): recorded weather data.
            datetime (datetime): UTC time of value. Defaults to None.
        """
        super().__init__(datetime=datetime)

        for key in METEOROLOGICAL:
            new_key = "_".join(METEOROLOGICAL[key]["label"].lower().split(" "))
            setattr(
                self,
                f"_{new_key}",
                ObservationStringDatum(values[key], METEOROLOGICAL[key]),
            ) if METEOROLOGICAL[key]["unit"] == "string" else setattr(
                self,
                f"_{new_key}",
                ObservationFloatDatum(values[key], METEOROLOGICAL[key]),
            )

    @property
    def wind_direction(self):
        """Return observed wind direction."""
        return self._wind_direction

    @property
    def wind_speed(self):
        """Return observed wind speed."""
        return self._wind_speed

    @property
    def wind_gust(self):
        """Return observed wind gust."""
        return self._wind_gust

    @property
    def wave_height(self):
        """Return observed wave height."""
        return self._wave_height

    @property
    def dominate_wave_period(self):
        """Return observed dominate wave period."""
        return self._dominate_wave_period

    @property
    def average_wave_period(self):
        """Return observed average wave period."""
        return self._average_wave_period

    @property
    def wave_direction(self):
        """Return observed wave direction."""
        return self._wave_direction

    @property
    def sea_level_pressure(self):
        """Return observed sea level pressure."""
        return self._sea_level_pressure

    @property
    def air_temperature(self):
        """Return observed air temperature."""
        return self._air_temperature

    @property
    def water_temperature(self):
        """Return observed water temperature."""
        return self._water_temperature

    @property
    def dewpoint_temperature(self):
        """Return observed dewpoint temperature."""
        return self._dewpoint_temperature

    @property
    def visibility(self):
        """Return observed visibility."""
        return self._visibility

    @property
    def pressure_tendency(self):
        """Return observed pressure tendency."""
        return self._pressure_tendency

    @property
    def tide(self):
        """Return observed tide."""
        return self._tide


class WaveSummaryObservation(BaseObservation):
    """Encapsulates `Buoy` wave summary data."""

    def __init__(
        self,
        values: dict[WaveSummaryKey, str],
        datetime: datetime = None,
    ):
        """Initialize Observation record with relevant metadata.

        Args:
            values (dict[str,str]): recorded weather data.
            datetime (datetime): UTC time of value. Defaults to None.
        """
        super().__init__(datetime=datetime)

        for key in WAVE_SUMMARY:
            new_key = "_".join(WAVE_SUMMARY[key]["label"].lower().split(" "))
            setattr(
                self,
                f"_{new_key}",
                ObservationStringDatum(values[key], WAVE_SUMMARY[key]),
            ) if WAVE_SUMMARY[key]["unit"] == "string" else setattr(
                self,
                f"_{new_key}",
                ObservationFloatDatum(values[key], WAVE_SUMMARY[key]),
            )

    @property
    def significant_wave_height(self):
        """Return observed wave height."""
        return self._significant_wave_height

    @property
    def swell_height(self):
        """Return observed swell height."""
        return self._swell_height

    @property
    def swell_period(self):
        """Return observed swell period."""
        return self._swell_period

    @property
    def wind_wave_height(self):
        """Return observed wind wave height."""
        return self._wind_wave_height

    @property
    def wind_wave_period(self):
        """Return observed wind wave period."""
        return self._wind_wave_period

    @property
    def swell_direction(self):
        """Return observed swell direction."""
        return self._swell_direction

    @property
    def wind_wave_direction(self):
        """Return observed wind wave direction."""
        return self._wind_wave_direction

    @property
    def steepness(self):
        """Return observed wave steepness."""
        return self._steepness

    @property
    def average_wave_period(self):
        """Return observed average wave period."""
        return self._average_wave_period

    @property
    def dominant_wave_direction(self):
        """Return observed direction of waves at dominant period."""
        return self._dominant_wave_direction
