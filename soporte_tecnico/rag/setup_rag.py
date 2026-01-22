from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_core.documents import Document

from soporte_tecnico.config import *


class SetupRAG:

    def __init__(self, docs_path: str = "docs", chroma_path: str = "./chroma_db"):
        self.docs_path = str(Path(docs_path))
        self.chroma_path = str(Path(chroma_path))
        self.embedding = OpenAIEmbeddings(model=MODEL_EMBEDDING)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 100
        )

    
    def load_documents(self) :

        print("Iniciando cargador de Dcoumentos")
        loader = DirectoryLoader(
            path=self.docs_path,
            glob="*.pdf",
            show_progress=True,
            loader_cls= PyPDFLoader
        )

        documents = loader.load()

        #Enriquecer metadatos
        for doc in documents:
            filename = Path(doc.metadata['source']).stem #mantiene solo el nombre del archivo
            doc.metadata.update({
                "filename": filename
            })
        
        return documents
    




