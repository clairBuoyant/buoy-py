from datetime import datetime as dt
from typing import Optional
from xml.etree.ElementTree import Element, fromstring

from pybuoy.api.base import ApiBase
from pybuoy.const import API_PATH, Endpoints
from pybuoy.observation.observation import MeteorologicalPrediction
from pybuoy.observation.observations import MeteorologicalPredictions
from pybuoy.unit_mappings import MeteorologicalKey


# TODO: consider datetime utils to handle parsing
def parse_dt(timestamp: str | None):
    if timestamp is None:
        raise ValueError
    return dt.fromisoformat(timestamp)


class Forecasts(ApiBase):
    # https://graphical.weather.gov/xml/rest.php
    def get(self, lat: float, lon: float, beginDate: str, endDate: str):
        # TODO: (LOW) add error checking for dates
        # If not in ISO format throw user friendly exception
        response = self.make_request(
            API_PATH[Endpoints.FORECASTS.value],
            params={
                "whichClient": "NDFDgen",
                "lat": lat,
                "lon": lon,
                "product": "time-series",
                "begin": dt.fromisoformat(beginDate).isoformat(),
                "end": dt.fromisoformat(endDate).isoformat(),
                "Unit": "e",
                "wspd": "wspd",
                "wdir": "wdir",
                "waveh": "waveh",
                "wgust": "wgust",
                "Submit": "Submit",
            },
        )

        # TODO: (MEDIUM) Refactor code into parserMixin?
        data = fromstring(response)

        wind_speed_sustained: Optional[Element] = data.find(".//*[@type='sustained']")
        wind_speed_sustained_values = self.__get_values(wind_speed_sustained, "value")

        wind_speed_gust: Optional[Element] = data.find(".//*[@type='gust']")
        wind_speed_gust_values: list[str] = self.__get_values(wind_speed_gust, "value")

        wind_direction: Optional[Element] = data.find(".//direction")
        wind_direction_values: list[str] = self.__get_values(wind_direction, "value")

        water_state: Optional[Element] = data.find(".//water-state")
        waves = water_state.find("waves") if water_state is not None else None
        wave_values: list[str] = self.__get_values(waves, "value")

        # mapping data to timestamp elements
        element_mappings = []
        time_layouts: list[Element] = data.findall(".//time-layout")
        for time_layout in time_layouts:
            if time_layout is None:
                continue
            layout_key: str | None = getattr(
                time_layout.find("layout-key"), "text", None
            )
            mapping: dict = {time_layout: {}}
            if (
                wind_speed_sustained is not None
                and layout_key == wind_speed_sustained.attrib["time-layout"]
            ):
                mapping[time_layout][
                    MeteorologicalKey.WSPD
                ] = wind_speed_sustained_values
            if (
                wind_speed_gust is not None
                and layout_key == wind_speed_gust.attrib["time-layout"]
            ):
                mapping[time_layout][MeteorologicalKey.GST] = wind_speed_gust_values
            if (
                wind_direction is not None
                and layout_key == wind_direction.attrib["time-layout"]
            ):
                mapping[time_layout][MeteorologicalKey.WDIR] = wind_direction_values
            if (
                water_state is not None
                and layout_key == water_state.attrib["time-layout"]
            ):
                mapping[time_layout][MeteorologicalKey.WVHT] = wave_values
            element_mappings.append(mapping)

        timed_mappings = []
        for element_mapping in element_mappings:
            time_layout = next(iter(element_mapping))
            time_stamps = self.__get_values(time_layout, "start-valid-time")
            mapping_holder = {}
            for i, time_stamp in enumerate(time_stamps):
                forecast_values = {
                    MeteorologicalKey.WSPD: "nan",
                    MeteorologicalKey.GST: "nan",
                    MeteorologicalKey.WDIR: "nan",
                    MeteorologicalKey.WVHT: "nan",
                }

                if MeteorologicalKey.WSPD in element_mapping[time_layout]:
                    forecast_values[MeteorologicalKey.WSPD] = element_mapping[
                        time_layout
                    ][MeteorologicalKey.WSPD][i]
                if MeteorologicalKey.GST in element_mapping[time_layout]:
                    forecast_values[MeteorologicalKey.GST] = element_mapping[
                        time_layout
                    ][MeteorologicalKey.GST][i]
                if MeteorologicalKey.WDIR in element_mapping[time_layout]:
                    forecast_values[MeteorologicalKey.WDIR] = element_mapping[
                        time_layout
                    ][MeteorologicalKey.WDIR][i]
                if MeteorologicalKey.WVHT in element_mapping[time_layout]:
                    forecast_values[MeteorologicalKey.WVHT] = element_mapping[
                        time_layout
                    ][MeteorologicalKey.WVHT][i]

                mapping_holder[time_stamp] = forecast_values
            timed_mappings.append(mapping_holder)

        synced_timed_mapping = self.__get_longest_mapping(timed_mappings)
        for timed_mapping in timed_mappings:
            for key in timed_mapping.keys():
                if timed_mapping[key][MeteorologicalKey.WSPD] != "nan":
                    synced_timed_mapping[key][MeteorologicalKey.WSPD] = timed_mapping[
                        key
                    ][MeteorologicalKey.WSPD]
                if timed_mapping[key][MeteorologicalKey.GST] != "nan":
                    synced_timed_mapping[key][MeteorologicalKey.GST] = timed_mapping[
                        key
                    ][MeteorologicalKey.GST]
                if timed_mapping[key][MeteorologicalKey.WDIR] != "nan":
                    synced_timed_mapping[key][MeteorologicalKey.WDIR] = timed_mapping[
                        key
                    ][MeteorologicalKey.WDIR]
                if timed_mapping[key][MeteorologicalKey.WVHT] != "nan":
                    synced_timed_mapping[key][MeteorologicalKey.WVHT] = timed_mapping[
                        key
                    ][MeteorologicalKey.WVHT]

        predictions = [
            MeteorologicalPrediction(synced_timed_mapping[key], dt.fromisoformat(key))
            for key in synced_timed_mapping.keys()
        ]

        return MeteorologicalPredictions(observations=predictions)

    def __get_values(self, element: Element | None, value: str) -> list[str]:
        if element is None:
            return []
        element_text_list: list = []
        element_list: list[Element] = element.findall(value)
        for element in element_list:
            element_text_list.append(element.text)
        return element_text_list

    def __get_longest_mapping(self, array: list[dict]) -> dict:
        index: int = 0
        max_len: int = 0
        for i, mapping in enumerate(array):
            if len(mapping.keys()) > max_len:
                index = i
                max_len = len(mapping.keys())
        return array.pop(index)

    def forecast_by_lat_lon(
        self,
        lat,
        lon,
        start_date: Optional[dt] = None,
        end_date: Optional[dt] = None,
        metric=False,
    ):
        return self._daily_forecast_from_location_info(
            location_info=[lat, lon],
            start_date=start_date,
            end_date=end_date,
            metric=metric,
        )

    def _daily_forecast_from_location_info(
        self,
        location_info,
        start_date: Optional[dt] = None,
        end_date: Optional[dt] = None,
        metric=False,
    ):
        if not start_date:
            start_date = dt.today()

        # TODO: test array of tuples
        # ? does order of query-string parameter matter
        lat, lon = location_info
        params = {
            "whichClient": "NDFDgen",
            "lat": lat,
            "lon": lon,
            "product": "time-series",
            "begin": start_date.isoformat(),
            "end": None if end_date is None else end_date.isoformat(),
            "Unit": "m" if metric else "e",
            "wspd": "wspd",
            "wdir": "wdir",
            "waveh": "waveh",
            "wgust": "wgust",
            "Submit": "Submit",
        }
        response = self.make_request(API_PATH[Endpoints.FORECASTS.value], params=params)
        xml_root = self._parse_xml(response)
        # TODO: complete
        return xml_root

    def __parse_conditions(self, tree: Element, condition: str):
        for weather_element in tree.iter(tag=condition):
            # TODO: list comprehension
            values = []

            # TODO: replace condition with another dynamic approach
            for condition_element in weather_element.iterfind(condition):
                # TODO: replace condition with another dynamic approach
                value = condition_element.attrib.get(condition)
                values.append(value)

            time_layout_key = weather_element.attrib["time-layout"]
            return time_layout_key, values

    def __parse_time_layouts(self, tree: Element):
        """Return a dictionary containing the time-layouts.

        A time-layout looks like:
            { 'time-layout-key': [(start-time, end-time), ...] }
        """
        time_layouts = {}
        for tl_elem in tree.iter(tag="time-layout"):
            start_times = []
            end_times = []
            for tl_child in tl_elem:
                if tl_child.tag == "layout-key":
                    key = tl_child.text
                elif tl_child.tag == "start-valid-time":
                    dt = parse_dt(tl_child.text)
                    start_times.append(dt)
                elif tl_child.tag == "end-valid-time":
                    dt = parse_dt(tl_child.text)
                    end_times.append(dt)
            # TODO: replace zip - lists not always symmetrical
            time_layouts[key] = zip(start_times, end_times)

        return time_layouts

    def _parse_xml(self, xml_data):
        return fromstring(xml_data)
