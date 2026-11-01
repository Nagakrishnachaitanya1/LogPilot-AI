
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()


# 1. Define the Pydantic model
class Student(BaseModel):
    name: str = Field(description="Student's name")
    marks: int = Field(description="Student's marks")
    result: str = Field(description="Pass or Fail")


# 2. Create the parser
parser = PydanticOutputParser(pydantic_object=Student)

# 3. Create the prompt
prompt = ChatPromptTemplate.from_template(
    "Analyze the following student information: {info}\n{format_instructions}"
)

# 4. Provide formatting instructions
prompt = prompt.partial(format_instructions=parser.get_format_instructions())

# print(parser)

# 5. Initialize the LLM
llm = ChatGroq(model="openai/gpt-oss-20b")

# 6. Create the chain
chain = prompt | llm | parser

# 7. Invoke the chain
response = chain.invoke({"info": "Krishna scored 90 marks and passed the examination."})

# 8. Access the structured output
print(response)
print(response.name)
print(response.marks)
print(response.result)
