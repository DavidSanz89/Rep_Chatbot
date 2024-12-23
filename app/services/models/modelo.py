from langchain_openai import ChatOpenAI
from config.settings import settings

def modelo():
    """
    Crea e instancia un modelo de ChatOpenAI.

    Este modelo se configura con los parámetros deseados, como el tipo de modelo y la temperatura.

    Returns:
        ChatOpenAI: Una instancia configurada del modelo GPT-4.
    """
    
    # Crear el modelo utilizando la clave API y configuraciones especificadas
    model = ChatOpenAI(model="gpt-4o", temperature=0, api_key=settings.openai_api_key)
    return model