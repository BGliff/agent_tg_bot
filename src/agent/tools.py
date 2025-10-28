from langchain_core.tools import tool

from agent.chains import ask_llm
from exceptions import WeatherError
from integrations.web_parser.integration import get_summary_by_url
from integrations.weather.integration import get_weather_by_location


@tool
async def multiply(a: int, b: int) -> int:
    """Умножает два числа"""
    return a * b


@tool
async def add(a: int, b: int) -> int:
    """Складывает два числа"""
    return a + b


@tool
async def get_page(url: str) -> str:
    """Извлекает html страницы по адресу url
        :param str url: url страницы
    """
    return await get_summary_by_url(url)


@tool
async def get_weather(location: str) -> str:
    """Возвращает информацию о погоде для локации location
        :param str location: локация
    """
    result = await get_weather_by_location(location)
    if result is None:
        msg = f"Не удалось получить данные о погоде для локации {location}"
        raise WeatherError(msg)

    return result


@tool
async def fallback(query: str) -> str:
    """Обращается к LLM в случае, если ни одна другая функция
        не подходит для обработки query
        :param str query: запрос пользователя, который будет пеереадресован LLM
    """
    return await ask_llm(query)
