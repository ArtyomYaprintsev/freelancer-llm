import os
from typing import Callable
from pydantic import BaseModel, Field


def _get_boolean_env(env_var: str):
    return os.getenv(env_var) in ["t", "1", "true", "True"]


class Config(BaseModel):
    SQLALCHEMY_ECHO: bool = _get_boolean_env("SQLALCHEMY_ECHO")
    DATABASE_URL: str = Field(
        default=os.getenv("DATABASE_URL"),  # type: ignore
        validate_default=True,
    )
    GIGACHAT_API_KEY: str | None = Field(
        default=os.getenv("GIGACHAT_API_KEY"),
        validate_default=True,
    )


config = Config()
