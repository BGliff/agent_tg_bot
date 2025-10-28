import logging

from typing_extensions import Self


class BaseBotError(Exception):
    def __init__(self: Self, message: str, log_exc: bool = True) -> None:
        self.message = message
        super().__init__(message)

        if log_exc:
            logging.exception(message)


class WeatherError(BaseBotError):
    pass
