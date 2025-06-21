import re
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.engine import make_url
from sqlalchemy.schema import CreateTable
from langchain_gigachat import GigaChat
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage

from project.database import get_engine
from project.models import Freelancer


def _get_system_input(db_url: str):
    dialect = make_url(db_url).get_dialect()

    return (
        "Ты ответственный за таблицу `{tablename}` в `{dialect}`:\n\n"
        "```sql\n{table_ddl}\n```\n\n"
        "Примечание к таблице:\n"
        "- `experience_level` - содержит набор значений `Beginner`, "
        "`Intermediate`, `Expert`\n"
        "- `payment_method` - содержит набор значений `Bank Transfer`, "
        "`PayPal`, `Mobile Banking`, `Crypto`\n\n"
        "Данные взяты из открытого источника, в случае возникновения проблем "
        "в понимании задачи, обратись к ресурсу: "
        "https://www.kaggle.com/datasets/shohinurpervezshohan/freelancer-earnings-and-job-trends/data\n\n"
        "Твоей задачей является генерация SQL select-запроса, результат "
        "которого должен помочь тебе ответить на заданный вопрос (все вопросы "
        "будут связаны с используемой таблицей в базе данных).\n\n"
        "Взаимодействие должно происходить следующим образом:\n"
        "1. Я пришлю тебе вопрос в формате ```question<вопрос>```\n"
        "2. Твой ответ должен быть в формате ```sql<select-запрос>```\n"
        "3. На своей стороне я выполню данный запрос и верну его результат в "
        "формате ```result<результат>```\n"
        "4. Ты должен обработать этот результат и вернуть конкретный ответ на "
        "поставленный вопрос\n"
        "На этом взаимодействие закончится\n"
        "Если по какой-то причине ты не можешь ответить на поставленные "
        "вопрос, то в ответе ты должен вернуть ```error<причина ошибки>```\n\n"
    ).format(
        tablename=Freelancer.__tablename__,
        dialect=dialect.name,
        table_ddl=str(
            CreateTable(Freelancer.__table__).compile(  # type: ignore
                dialect=dialect(),
            )
        ).strip(),
    )


def _get_error_message(content: str) -> str | None:
    pattern = r"```error(?P<error>.+)```"
    matching = re.search(pattern, content, re.DOTALL)
    if matching:
        return matching.group("error")
    return None


def _get_select_query(content: str) -> str | None:
    pattern = r"```sql(?P<query>.+)```"
    matching = re.search(pattern, content, re.DOTALL)
    if matching:
        return matching.group("query")
    return None


def get_select_query(
    chat: GigaChat,
    *,
    messages: list[BaseMessage],
    debug: bool = False,
) -> tuple[str, BaseMessage]:
    query_response = chat.invoke(messages)

    if debug:
        print("Response\n", query_response)

    if not isinstance(query_response.content, str):
        raise ValueError(
            "Expected `str` type of the llm response, got "
            f"{type(query_response.content)}",
        )

    if error := _get_error_message(query_response.content):
        raise ValueError("The llm response contains an error: " + error)

    query = _get_select_query(query_response.content)

    if query is None:
        raise ValueError("The llm response does not contain a query")

    return query, query_response


def get_answer(
    chat: GigaChat,
    *,
    messages: list[BaseMessage],
    debug: bool = False,
) -> tuple[str, BaseMessage]:
    answer_response = chat.invoke(messages)

    if debug:
        print("Response\n", answer_response)

    if not isinstance(answer_response.content, str):
        raise ValueError(
            "Expected `str` type of the llm response, got "
            f"{type(answer_response.content)}",
        )

    if error := _get_error_message(answer_response.content):
        raise ValueError("The llm response contains an error: " + error)

    return answer_response.content, answer_response


def get_answer_to_question(
    question: str,
    *,
    apikey: str,
    db_url: str,
    debug: bool = False,
) -> str:
    chat = GigaChat(credentials=apikey, verify_ssl_certs=False)

    messages = [
        SystemMessage(_get_system_input(db_url)),
        HumanMessage(
            "Напиши SQL запрос для ответа на вопрос:\n\n"
            f"```question{question}```",
        ),
    ]

    query, message = get_select_query(chat, messages=messages, debug=debug)

    with Session(get_engine(db_url, echo=debug)) as session:
        select_result = str(list(session.execute(text(query)).all()))

    if debug:
        print("LLM query result\n", select_result)

    messages.append(message)
    messages.append(
        HumanMessage(
            "Напиши ответ на поставленный вопрос:\n\n"
            f"```question{question}```\n\n"
            "Учитывая результат SQL запроса:\n\n"
            f"```result{select_result}```"
        ),
    )

    answer, _ = get_answer(chat, messages=messages, debug=debug)

    return answer
