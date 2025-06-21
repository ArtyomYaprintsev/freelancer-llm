import pandas as pd
from pathlib import Path
from sqlalchemy import delete, insert, inspect
from sqlalchemy.orm import Session

from project.database import get_engine, Base
from project.models import Freelancer

from project.database.validate import validate


def setup(source: Path, db_url: str, debug: bool = False):
    is_valid = validate(
        db_url=db_url,
        debug=debug,
        raise_exception=False,
    )

    if not is_valid:
        with get_engine(db_url, echo=debug).connect() as conn:
            inspector = inspect(conn)

            if inspector.has_table(Freelancer.__tablename__):
                Base.metadata.drop_all(conn, tables=[Freelancer.__table__])  # type: ignore

            Base.metadata.create_all(conn, tables=[Freelancer.__table__])  # type: ignore

    df = pd.read_csv(source)

    with Session(get_engine(db_url, echo=debug)) as session:
        delete_stmt = delete(Freelancer)
        session.execute(delete_stmt)

        insert_stmt = insert(Freelancer).values(
            [
                {
                    Freelancer.id: row["Freelancer_ID"],
                    Freelancer.job_category: row["Job_Category"],
                    Freelancer.platform: row["Platform"],
                    Freelancer.experience_level: row["Experience_Level"],
                    Freelancer.client_region: row["Client_Region"],
                    Freelancer.payment_method: row["Payment_Method"],
                    Freelancer.job_completed: row["Job_Completed"],
                    Freelancer.earnings_USD: row["Earnings_USD"],
                    Freelancer.hourly_rate: row["Hourly_Rate"],
                    Freelancer.job_success_rate: row["Job_Success_Rate"],
                    Freelancer.client_ration: row["Client_Rating"],
                    Freelancer.job_duration_days: row["Job_Duration_Days"],
                    Freelancer.project_type: row["Project_Type"],
                    Freelancer.rehire_rate: row["Rehire_Rate"],
                    Freelancer.marketing_spend: row["Marketing_Spend"],
                }
                for _, row in df.iterrows()
            ]
        )
        session.execute(insert_stmt)

        session.commit()
