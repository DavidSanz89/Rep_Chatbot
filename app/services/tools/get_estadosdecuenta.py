from langchain.agents import tool
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-4o", temperature=0)

dni = "12345678"
email = "cesarf.landap@gmail.com"
mes = "agosto"
año = "2024"


def buscar_archivo(directorio_base):
    carpeta_dni = os.path.join(directorio_base, dni)
    nombre_archivo = f"{dni}_{mes}_{año}.pdf"
    ruta_archivo = os.path.join(carpeta_dni, nombre_archivo)
    
    if os.path.exists(ruta_archivo):
        return ruta_archivo
    else:
        return None


def enviar_correo(destinatario, asunto, cuerpo, archivo_adjunto):
    """
    Envía un correo electrónico con un archivo adjunto.

    Args:
        destinatario (str): Correo electrónico del destinatario.
        asunto (str): Asunto del correo.
        cuerpo (str): Cuerpo del correo.
        archivo_adjunto (str): Ruta del archivo a adjuntar.

    Returns:
        None
    """
    remitente = "davidsanzrioja@gmail.com"
    contraseña = "Westorne2716355@" # Considera usar un método más seguro para manejar contraseñas

    # Se crea un mensaje multiparte para el correo
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente # Establece el remitente del correo
    mensaje['To'] = destinatario # Establece el destinatario del correo
    mensaje['Subject'] = asunto # Establece el asunto del correo


    # Adjunta el cuerpo del mensaje
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    # Abre el archivo adjunto en modo binario
    with open(archivo_adjunto, "rb") as adjunto:
        parte = MIMEBase('application', 'octet-stream')
        parte.set_payload(adjunto.read()) # Lee el contenido del archivo adjunto
        encoders.encode_base64(parte) # Codifica el archivo en base64 para el envío
        parte.add_header(
            'Content-Disposition',
            f"attachment; filename= {os.path.basename(archivo_adjunto)}",  # Establece el nombre del archivo adjunto
        )
        mensaje.attach(parte) # Adjunta el archivo al mensaje

    # Configura el servidor SMTP para enviar el correo
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()
    servidor.login(remitente, contraseña)
    texto = mensaje.as_string()
    servidor.sendmail(remitente, destinatario, texto)
    servidor.quit() # Cierra la conexión al servidor


def manejar_consulta(carpeta):
    """
    Maneja la consulta para enviar el estado de cuenta al correo.

    Returns:
        str: Mensaje sobre el estado del envío del estado de cuenta.
    """
    
    carpeta = "C:/Users/LENOVO/Desktop/Robotics/Curso Chatbot/Replica_chatbot/app/data/estados_de_cuenta"
    #Se define la ruta de la carpeta donde se almacenan los estados de cuenta

    archivo = buscar_archivo(carpeta)
    # Se busca el archivo correspondiente en la carpeta especificada
    if archivo:
        # Si se encuentra el archivo, se define el asunto y el cuerpo del correo
        asunto = "Tu Estado de Cuenta"
        cuerpo = f"Adjunto encontrarás tu estado de cuenta del mes de {mes} de {año}."
        # Se envía el correo con el archivo adjunto
        enviar_correo(email, asunto, cuerpo, archivo)
        return "El estado de cuenta ha sido enviado a tu correo."
    else:
        # Si no se encuentra el archivo, se retorna un mensaje de error
        return "No se encontró un estado de cuenta para esos datos."



# Plantilla para el modelo
prompt = PromptTemplate.from_template("""
    El usuario ha hecho la siguiente consulta:
    {consulta}

    Por favor, extrae la siguiente información:
    - Año (un año de 4 dígitos)
    - Email (una dirección de correo electrónico válida)

    Responde en el siguiente formato:
    DNI: {dni}
    Mes: {mes}
    Año: {año}
    Email: {email}
    """)


directorio_base = "C:/Users/LENOVO/Desktop/Robotics/Curso Chatbot/Replica_chatbot/app/data/estados_de_cuenta"

@tool
def get_bank_statements(
    mes: str = None,
    año: str = None,
) -> str:
    """Use this tool to send account statements by email"""
    if not mes or not año:
        missing_info = []
        # Verifica si falta el mes y/o el año
        if not mes:
            missing_info.append("mes") 
        if not año:
            missing_info.append("año") 

        return f"Faltan datos para procesar la solicitud. Por favor, proporciona lo siguiente: {', '.join(missing_info)}."
        
    archivo = manejar_consulta(directorio_base)
    if archivo:
        # Si se encuentra el archivo, define el asunto y cuerpo del correo
        asunto = "Tu Estado de Cuenta"
        cuerpo = f"Adjunto encontrarás tu estado de cuenta del mes de {mes} de {año}."
        # Envía el correo con el archivo adjunto
        enviar_correo(email, asunto, cuerpo, archivo)
        return "Se envió satisfactoriamente el estado de cuenta a su correo."
    else:
        # Si no se encuentra el archivo, retorna un mensaje de error
        return "No se encontró un estado de cuenta para esos datos."
    
    
#response = get_bank_statements.invoke("enviame mi estado de cuenta a mi correo")
#print(response)


