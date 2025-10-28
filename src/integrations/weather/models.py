from pydantic import BaseModel, Field


class Location(BaseModel):
    location_id: int = Field(alias="id")


class FindResponse(BaseModel):
    locations_list: list[Location] = Field(alias="list", min_length=1)


class Sys(BaseModel):
    country: str


class WeatherDescription(BaseModel):
    description: str


class Wind(BaseModel):
    speed: int


class WeatherSummary(BaseModel):
    temp: float
    temp_max: float
    temp_min: float


class WeatherResponse(BaseModel):
    name: str
    sys: Sys
    weather: list[WeatherDescription] = Field(min_length=1)
    main: WeatherSummary
    wind: Wind

    def to_pretty_string(self):
        return (
            f"Город: {self.name} {self.sys.country}\n"
            f"Видимость: {self.weather[0].description}\n"
            f"Температура: {self.main.temp}\n"
            f"Максимальная температура: {self.main.temp_max}\n"
            f"Минимальная температура: {self.main.temp_min}\n"
            f"Ветер: {self.wind.speed} м/с"
        )
