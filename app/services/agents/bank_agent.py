from services.tools.bdrelacional import get_query_database
from services.tools.bd_vectorial import get_qa_bank
from services.tools.get_estadosdecuenta import get_bank_statements
from services.tools.consultas_estadosdecuenta import query_pdf_tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-4o", temperature=0)

memory = MemorySaver()

tools = [ get_query_database, get_qa_bank, query_pdf_tool, get_bank_statements]
#tools = [ get_query_database, query_pdf_tool, get_bank_statements]


# Mensaje que se proporciona al agente como modificador de estado
prompt ='''Please answer in Spanish, You are a very powerful assistant, but if the tools don't know the answer, it means that you don't know either.'''

graph = create_react_agent(model, tools=tools, state_modifier=prompt, checkpointer=memory)

