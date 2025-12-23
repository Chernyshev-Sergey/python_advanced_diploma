from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB__")

    url: str
    echo: int
    password: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.test"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    db: DatabaseConfig


settings = Settings()  # type: ignore[call-arg]
