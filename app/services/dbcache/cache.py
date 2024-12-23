import chromadb
import uuid
from loguru import logger
from chromadb.config import Settings

# Inicializar el cliente de ChromaDB y crear o acceder a la colección 'dbcache'
chroma_client = chromadb.Client(Settings(persist_directory="C:/Users/LENOVO/Desktop/Robotics/Curso Chatbot/Replica_chatbot/app/data/chroma_langchain_db/chroma_langchain_db"))
collection = chroma_client.get_or_create_collection(name="dbcache")

def check_cache(question):

    cache_result = collection.query(
        query_texts=[question],
        n_results=1
    )

    if not cache_result["documents"] or not cache_result["documents"][0]:
        logger.info('No hit in cache')
        return None
    
    distance = cache_result["distances"][0][0]
    if distance > 0.7:
        logger.info(f'Cache results distant: [{distance}]')
        return None

    answer = cache_result["metadatas"][0][0].get('answer')
    if answer:
        logger.info(f'Cache hit: [{distance}] {answer[:30]}...')
        return answer + '\n\n`cached`'
    
    logger.info('No answer found in cache metadata')
    return None


def save_answer(question, response):

    logger.info(f"Saving to cache: {question[:30]}...") 
    random_id = str(uuid.uuid4())[:8] 
    
    collection.add(
        documents=[question],
        ids=[random_id],
        metadatas=[{"answer": response}]
    )
    logger.info(f"Saved response for question: {question[:30]}...") 
    return None



