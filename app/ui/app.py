import sys
import os

# Agrega la carpeta raíz (app) al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import streamlit as st
from langgraph.checkpoint.memory import MemorySaver
from services.agents.bank_agent import graph
#from services.dbcache.cache import check_cache, save_answer

memory = MemorySaver()


def format_message(message, message_type):
    """Formatea el mensaje según su tipo (HUMANO o AI).

    Args:
        message: Un objeto que contiene el contenido del mensaje.
        message_type: Un string que indica el tipo de mensaje, que puede ser:
                      - "HUMANMESSAGE": Indica que el mensaje es del usuario.
                      - "AIMESSAGE": Indica que el mensaje es de la IA.
    """
    if message_type == "HUMANMESSAGE":
        return f"**🧑 Usted:** {message.content}"
    elif message_type == "AIMESSAGE" and message.content.strip():
        return f"**🤖 AI:** {message.content}"
    else:
        return None
    


# Título de la aplicación
st.title("Chatbot Bancario")

# Campo de entrada para el usuario
user_input = st.text_input("Escribe tu mensaje:")
#user_input="cuáles son los Servicios asociados a la Tarjeta de Crédito en caja cusco"


# Botón para enviar el mensaje
if st.button("Enviar") and user_input:

                msg = f"{user_input}"
                response = graph.invoke(
                    input={"messages": msg},
                    config={
                        "configurable": {
                            "thread_id": "1",    
                        }
                    }
                )
                #st.write(response)
# Obtener el último mensaje de la respuesta
                last_message = response["messages"][-1]
                formatted_message = format_message(last_message, type(last_message).__name__.upper())
                    
                # Mostrar el mensaje formateado
                if formatted_message:
                        st.markdown(formatted_message)
