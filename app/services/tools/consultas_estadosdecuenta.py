import pdfplumber
import os
from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema import Document
from langchain_openai import ChatOpenAI
# Instanciar el modelo de OpenAI
#model = modelo()
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#os.environ["OPENAI_API_KEY"] = "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"
model = ChatOpenAI(model="gpt-4o", temperature=0)

dni = "12345678"
mes = "agosto"
año = "2024"

# Directorio base donde se encuentran los estados de cuenta
base_dir = "C:/Users/LENOVO/Desktop/Robotics/Curso Chatbot/Replica_chatbot/app/data/estados_de_cuenta"


def extract_text_from_pdf(pdf_path):
    """
    Extrae el texto de un archivo PDF.
    Args:
        pdf_path (str): Ruta del archivo PDF.
    Returns:
        str: Contenido de texto extraído del PDF.
    """
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text


@tool
def query_pdf_tool(query):
    '''Use this tool to check your bank account status and answer user questions.'''
    
    """
    Herramienta para consultar el estado de cuenta y responder preguntas del usuario.
    Args:
        query (str): Pregunta que el usuario desea hacer sobre su estado de cuenta.

    Returns:
        str: Respuesta generada a partir del contenido del PDF.
    """
    dni = "12345678"
    mes = "agosto"
    año = "2024"

    # Condición que indica que como datos obligatorios deben ser mes y año
    if mes is None:
       mes = input("Por favor, ingrese el mes (formato: mes): ")
    if año is None:
       año = input("Por favor, ingrese el año (formato: año): ")

    # Generar el nombre del archivo PDF a partir del DNI, mes y año
    pdf_filename = f"{dni}_{mes}_{año}.pdf"
    pdf_path = os.path.join(base_dir, dni, pdf_filename)

    # Extraer texto del PDF
    text = extract_text_from_pdf(pdf_path)

    # Crear un documento con el contenido extraído
    document = Document(page_content=text, metadata={})

    # Crear una plantilla de prompt para la consulta
    prompt = ChatPromptTemplate.from_messages(
        [("system", "El siguiente es el contenido del estado de cuenta:\n{context}\n\nPregunta: {query}\nRespuesta:")]
    )

    # Crear una cadena para procesar el documento y la consulta
    chain = create_stuff_documents_chain(model, prompt)

    try:
        # Invocar la cadena con el documento y la consulta
        result = chain.invoke({"context": [document], "query": query})
    except AttributeError as e:
        print(f"AttributeError: {e}")
        return str(e)

    return result


response = query_pdf_tool.invoke("cual es el pago minimo")
print(response)

