from dotenv import load_dotenv
from pathlib import Path

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from app.schemas.incident import LogAnalysisResponse
from app.db.database import create_table, insert

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path, override=True)

create_table()

parser = PydanticOutputParser(pydantic_object=LogAnalysisResponse)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are LogPilot AI, an expert software debugging assistant.

            Your task is to analyze application logs, Python exceptions,
            and stack traces.

            Generate a structured debugging report following these rules:

            1. Identify the error category and severity.
            2. Explain the error in simple, understandable language.
            3. Identify the most likely root cause based on available evidence.
            4. List other possible causes when relevant.
            5. Recommend practical debugging steps.
            6. Extract relevant evidence directly from the provided logs.
            7. Assign a confidence level to your analysis.
            8. Never invent information that is not supported by the logs.
            9. Acknowledge uncertainty when the logs provide insufficient evidence.

            Follow these output formatting instructions carefully:

            {format_instructions}
            """,
        ),
        (
            "human",
            """
            Analyze the following application logs:

            {log_text}
            """,
        ),
    ]
)


prompt = prompt.partial(format_instructions=parser.get_format_instructions())


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)


chain = prompt | llm | parser


def analyze_logs(log_text: str) -> LogAnalysisResponse:
    analysis = chain.invoke({"log_text": log_text})

    insert(log_text, analysis.model_dump_json())

    return analysis


if __name__ == "__main__":
    sample_log = """
    Traceback (most recent call last):
      File "app.py", line 10, in connect
        connection = sqlite3.connect("database.db")

    sqlite3.OperationalError:
    unable to open database file
    """

    answer = analyze_logs(sample_log)

    # print(answer.model_dump_json(indent=2))
