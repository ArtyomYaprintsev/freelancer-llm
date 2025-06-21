import typer
from pathlib import Path
from typing import Annotated

from project.database import validate, setup
from project.services.gigachat import get_answer_to_question


def main(
    question: Annotated[
        str,
        typer.Argument(
            help="Question that relates with the `freelancers` table.",
        ),
    ],
    apikey: Annotated[str, typer.Option(help="GigaChat API Key.")],
    debug: Annotated[bool, typer.Option(help="Show debug info.")] = False,
    db_url: Annotated[
        str,
        typer.Option(help="Database URL."),
    ] = "sqlite:///./db.sqlite3",
    source: Annotated[
        Path,
        typer.Option(
            help="Dataset filename. Required if the `autosetup` is enabled.",
        ),
    ] = (Path(__file__).parent / "freelancer_earnings_bd.csv"),
    autosetup: Annotated[
        bool,
        typer.Option(help="Enable auto setup before running."),
    ] = True,
):
    if autosetup:
        setup(source=source, db_url=db_url, debug=debug)
    else:
        validate(db_url=db_url, debug=debug, raise_exception=True)

    print(
        get_answer_to_question(
            question=question,
            apikey=apikey,
            db_url=db_url,
            debug=debug,
        ),
    )


if __name__ == "__main__":
    typer.run(main)
