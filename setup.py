import typer
from pathlib import Path
from typing import Annotated

from project.utils import setup as setup_database


def setup(
    source: Annotated[
        Path,
        typer.Option(help="Dataset filename."),
    ] = (Path(__file__).parent / "freelancer_earnings_bd.csv"),
    db_url: Annotated[
        str,
        typer.Option(help="Database URL."),
    ] = "sqlite:///./db.sqlite3",
    debug: Annotated[bool, typer.Option(help="Show debug info.")] = False,
):
    setup_database(source=source, db_url=db_url, debug=debug)


if __name__ == "__main__":
    typer.run(setup)
