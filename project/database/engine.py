from functools import lru_cache
from sqlalchemy import create_engine

from project.config import config


@lru_cache()
def get_engine():
    return create_engine(
        url=config.DATABASE_URL,
        echo=config.SQLALCHEMY_ECHO,
    )
