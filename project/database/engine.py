from functools import lru_cache
from sqlalchemy import create_engine


@lru_cache()
def get_engine(url: str, echo: bool):
    return create_engine(url=url, echo=echo)
