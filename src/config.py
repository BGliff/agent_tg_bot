from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentTGBotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env", env_file_encoding="utf-8", extra="ignore"
    )


class AgentConfig(AgentTGBotSettings):
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str
    OPENROUTER_MODEL_NAME: str


class BotConfig(AgentTGBotSettings):
    BOT_TOKEN: str


class OpenWeatherConfig(AgentTGBotSettings):
    OPENWEATHER_APP_ID: str
    OPENWEATHER_BASE_URL: str


AGENT_CONFIG = AgentConfig()
BOT_CONFIG = BotConfig()
OPENWEATHER_CONFIG = OpenWeatherConfig()
