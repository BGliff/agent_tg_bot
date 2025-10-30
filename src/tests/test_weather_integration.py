import aiohttp
import pytest

from typing import Any, Optional, Union
from typing_extensions import Self
from yarl import URL

import integrations.weather.integration as integration


class WeatherDataMocks:
    VALID_FIND_RESPONSE = {
        "list": [
            {
                "id": 1000,
            }
        ],
    }
    INVALID_FIND_RESPONSE: dict[str, Any] = {}

    VALID_WEATHER_RESPONSE = {
        "name": "Москва",
        "sys": {
            "country": "RU",
        },
        "weather": [
            {
                "description": "небольшая морось",
            },
        ],
        "main": {
            "temp": 8.14,
            "temp_max": 8.19,
            "temp_min": 8.05,
        },
        "wind": {
            "speed": 4.1,
        },
    }
    INVALID_WEATHER_RESPONSE: dict[str, Any] = {}

    PRETTY_WEATHER_STRING = (
        "Город: Москва RU\n"
        "Видимость: небольшая морось\n"
        "Температура: 8.14\n"
        "Максимальная температура: 8.19\n"
        "Минимальная температура: 8.05\n"
        "Ветер: 4.1 м/с"
    )


class MockResponse:
    def __init__(self: Self, obj: dict[str, Any]) -> None:
        self.obj = obj

    def __call__(
        self: Self,
        url: Union[str, URL],
        **kwargs: Any,
    ) -> Self:
        return self

    async def __aenter__(self: Self) -> Self:
        return self

    async def __aexit__(
            self: Self,
            exc_type: Any,
            exc: Any,
            tb: Any,
    ) -> None:
        pass

    async def json(self: Self) -> dict[str, Any]:
        return self.obj


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("mock", "expected_result"),
    [
        (MockResponse(WeatherDataMocks.VALID_FIND_RESPONSE), WeatherDataMocks.VALID_FIND_RESPONSE["list"][0]["id"]),
        (MockResponse(WeatherDataMocks.INVALID_FIND_RESPONSE), None),
    ],
)
async def test_get_location_id(
    mock: MockResponse,
    expected_result: Optional[int],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(aiohttp.ClientSession, "get", mock)
    async with aiohttp.ClientSession() as session:
        assert (
            await integration.get_location_id(session, "Москва")
            == expected_result
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("mock", "expected_result"),
    [
        (MockResponse(WeatherDataMocks.VALID_WEATHER_RESPONSE), WeatherDataMocks.PRETTY_WEATHER_STRING),
        (MockResponse(WeatherDataMocks.INVALID_WEATHER_RESPONSE), None),
    ],
)
async def test_get_weather_by_location_id(
    mock: MockResponse,
    expected_result: Optional[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(aiohttp.ClientSession, "get", mock)
    async with aiohttp.ClientSession() as session:
        assert (
            await integration.get_weather_by_location_id(session, 1000)
            == expected_result
        )
