from pandasai.connectors import PostgreSQLConnector
from pandasai import SmartDataframe
from langchain_core.tools import tool
from dotenv import load_dotenv
import os


load_dotenv()

PANDASAI_API_KEY = os.getenv("PANDASAI_API_KEY")

# Init PandasAI Smart Dataframe
postgres_connector__accounts = PostgreSQLConnector(
    config={
        "host": "db",
        "port": 5432,
        "database": "data_bank",
        "username": "postgres",
        "password": "12345678",
        "table": "cuentas",
        }
)

try:
    df_cuentas = SmartDataframe(postgres_connector__accounts)
   
    @tool
    def get_query_database(consulta: str) -> int:
        """Use this tool to query bank transactions and balances in a DataFrame.
        The query is processed using Pandas AI to analyze the data and return an
        answer based on the available information.
        """
        return df_cuentas.chat(consulta)


    #response = get_query_database.invoke("Dame las transacciones del mes de junio 2017 de la cuenta 409000611074")
    #print(response)


finally:
    # Cerrar conexión si el conector tiene un método close()
    if hasattr(postgres_connector__accounts, "close"):
        postgres_connector__accounts.close()

