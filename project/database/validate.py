from sqlalchemy import inspect, select
from sqlalchemy.orm import Session

from project.database import get_engine
from project.models import Freelancer


def validate(
    db_url: str,
    debug: bool = False,
    raise_exception: bool = True,
) -> bool:
    with get_engine(db_url, echo=debug).connect() as conn:
        inspector = inspect(conn)

        if inspector.has_table(Freelancer.__tablename__):
            try:
                with Session(conn) as session:
                    session.execute(select(Freelancer).limit(1))
            except Exception as exc:
                if raise_exception:
                    raise ValueError(
                        "smth wrong with table, original error above: ", exc
                    )
                else:
                    return False
            return True

        if raise_exception:
            raise ValueError("table is missing")
        else:
            return False

    return True
