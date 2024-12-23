from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
import re
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#os.environ["OPENAI_API_KEY"] = "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"

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=768
)

def limpiar_texto(texto):
    texto = re.sub(r'\s+', ' ', texto)
    texto = re.sub(r'•|·|-|\*|•|\u2022', '', texto)
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto.strip()


model = ChatOpenAI(model="gpt-4o", temperature=0)



def summarize_and_add_metadata(pages, pdf_filename, folder):
    prompt = ChatPromptTemplate.from_messages(
        [("system", "Write a concise summary of the following:\\n\\n{context}")]
    )

    chain = create_stuff_documents_chain(model, prompt)
    result = chain.invoke({"context": pages})

    text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=0)
    splits = text_splitter.split_documents(pages)

    #summary = read_summary_file(pdf_filename, folder)

    for split in splits:
        if not split.metadata:
            split.metadata = {}
        split.metadata.update({"resumen": result,"name":pdf_filename,"source":folder})

    return splits   


ruta_carpeta = "C:\\Users\\LENOVO\\Desktop\\Robotics\\Curso Chatbot\\Replica_chatbot\\app\\data\\Corpus"
all_splits = []

for archivo in os.listdir(ruta_carpeta):
    if archivo.endswith(".pdf"):
        ruta_pdf = os.path.join(ruta_carpeta, archivo)
        loader = PyPDFLoader(ruta_pdf)
        pages = loader.load_and_split()
        cleaned_pages = [Document(page_content=limpiar_texto(page.page_content), metadata=page.metadata) for page in pages]
        splits = summarize_and_add_metadata(cleaned_pages, archivo, ruta_pdf)       
        all_splits.extend(splits)



vectorstore = Chroma.from_documents(
    collection_name="corpus_tokens", 
    documents=all_splits, 
    embedding=embeddings, 
    persist_directory="C:/Users/LENOVO/Desktop/Robotics/Curso Chatbot/Replica_chatbot/app/data/chroma_langchain_db"
)

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})





