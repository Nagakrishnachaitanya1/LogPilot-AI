from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from app.schemas.incident import LogAnalysisResponse


load_dotenv()


parser = PydanticOutputParser(pydantic_object=LogAnalysisResponse)

prompt = ChatPromptTemplate.from_template(
    """Analyze the following application logs:

{log_text}

Follow these formatting instructions carefully:

{format_instructions}

You are LogPilot AI, an expert software debugging assistant.

Your task is to analyze application logs, Python exceptions, and stack traces.

Analyze the provided logs and generate a structured debugging report.

Follow these rules:
1. Identify the error category and severity.
2. Explain the error in simple, understandable language.
3. Identify the most likely root cause based on the available evidence.
4. List other possible causes when relevant.
5. Recommend practical debugging steps.
6. Extract relevant evidence directly from the provided logs.
7. Assign a confidence level to your analysis.
8. Never invent information that is not supported by the logs.
9. If the logs do not provide enough information, explicitly acknowledge the uncertainty.
10. Follow the output formatting instructions provided below.
"""
)

prompt = prompt.partial(format_instructions=parser.get_format_instructions())

llm = ChatGroq(model="openai/gpt-oss-20b")

chain = prompt | llm | parser

answer = chain.invoke(
    {
        "log_text": """Traceback (most recent call last):
  File "app.py", line 10, in connect
    connection = sqlite3.connect("database.db")
sqlite3.OperationalError: unable to open database file""",
    }
)

print(answer)
