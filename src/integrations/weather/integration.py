import aiohttp

from pydantic import ValidationError
from typing import Optional

from config import OPENWEATHER_CONFIG
from integrations.weather.models import WeatherResponse, FindResponse


async def get_location_id(session: aiohttp.ClientSession, location: str) -> Optional[int]:
    async with session.get(
        f"{OPENWEATHER_CONFIG.OPENWEATHER_BASE_URL}/find",
        params={
            'q': location,
            'type': 'like',
            'units': 'metric',
            'lang': 'ru',
            'APPID': OPENWEATHER_CONFIG.OPENWEATHER_APP_ID,
        }
    ) as response:
        data = await response.json()

    try:
        find_response = FindResponse.model_validate(data, by_alias=True)
    except ValidationError:
        return None
    return find_response.locations_list[0].location_id


async def get_weather_by_location_id(session: aiohttp.ClientSession, location_id: int) -> Optional[str]:
    async with session.get(
        f"{OPENWEATHER_CONFIG.OPENWEATHER_BASE_URL}/weather",
        params={
            'id': location_id,
            'units': 'metric',
            'lang': 'ru',
            'APPID': OPENWEATHER_CONFIG.OPENWEATHER_APP_ID,
        }
    ) as response:
        data = await response.json()

    try:
        weather_response = WeatherResponse.model_validate(data)
    except ValidationError:
        return None

    return weather_response.to_pretty_string()


async def get_weather_by_location(location: str) -> Optional[str]:
    async with aiohttp.ClientSession() as session:
        location_id = await get_location_id(session, location)
        if location_id is None:
            return None
        return await get_weather_by_location_id(session, location_id)
