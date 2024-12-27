from langchain.agents import tool
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from loguru import logger
from langchain_openai import ChatOpenAI
import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-4o", temperature=0)
    
# Inicializar embeddings de OpenAI
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=768
)

vectorstore = Chroma(collection_name="corpus_tokens", embedding_function=embeddings, persist_directory = "./app/data/chroma_langchain_db")
retriever = vectorstore.as_retriever()

# Definir el prompt del sistema para el asistente
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "Answer in Spanish"
    "\n\n"
    "{context}"
)

# Crear plantilla de prompt para las preguntas
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)



# Crear cadena de preguntas y respuestas
question_answer_chain = create_stuff_documents_chain(model, prompt)

# Crear la cadena de recuperación y generación de respuestas
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

logger.info(f"rag_chain type={type(rag_chain)}")


@tool
def get_qa_bank(consulta):
    """Use this tool when the user makes queries related to procedures, applications such as Yape, products or banking regulations that are documented in the available guides or reports. Answer the query of any banking entity."""
    
    response = rag_chain.invoke({"input": consulta })
    return response["answer"] 


#response = get_qa_bank.invoke("cuáles son los Servicios asociados a la Tarjeta de Crédito en caja cusco")
#print(response)



