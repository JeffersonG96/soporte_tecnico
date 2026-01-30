from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_core.documents import Document
from langchain_chroma import Chroma

from soporte_tecnico.config import *


class SetupRAG:

    def __init__(self, docs_path: str = "docs", chroma_path: str = "./chroma_db"):
        self.docs_path = str(Path(docs_path))
        self.chroma_path = Path(chroma_path)
        self.embedding = OpenAIEmbeddings(model=MODEL_EMBEDDING)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 360,
            chunk_overlap = 60
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
            filename = Path(doc.metadata['source']).stem.replace('_',' ') #mantiene solo el nombre del archivo
            doc.metadata.update({
                "filename": filename
            })
        
        return documents
    
    def splitter_documents(self, documents: list[Document]) -> list[Document]:
        """Divide los documentos en chunks"""

        chunks = self.text_splitter.split_documents(documents)

        #Enriquecer metadatos de chunks
        for i,chunk in enumerate(chunks):
            chunk.metadata.update({
                "chunk_id":i,
                "chunk_size": len(chunk.page_content)
            })
        
        return chunks
    
    def ceate_vectorstore(self, documents: list[Document]) -> Chroma:
        """Crea los embeddings y guarda en Chroma"""

        if self.chroma_path.exists():
            import shutil
            print("Eliminando directorio existente de Chroma")
            shutil.rmtree(path = str(self.chroma_path))
        
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embedding,
            collection_name="openai_knowledge",
            persist_directory=str(self.chroma_path)
        )

        return vectorstore
    
    def load_existing_vectorstore(self):
        """Consultar a una vectorstore existente"""
        if self.chroma_path.exists():
            raise FileNotFoundError(f"ERROR: no se encontro vectorstore en: {self.chroma_path}")
        
        vectorstore = Chroma(
            collection_name="openai_knowledge",
            embedding_function= self.embedding,
            persist_directory=str(self.chroma_path)
        )

        return vectorstore
    
    def setup_rag(self, force_rebuild: bool= False):
        """Configura le sistema RAG"""

        if self.chroma_path.exists() and not force_rebuild:
            print("Vectorstore encontrado")
            return self.load_existing_vectorstore()
        
        #Cargar los archivos pdf
        documents = self.load_documents()

        #Dividir los documents
        print("Dividiendo en Chunks")
        chunks = self.splitter_documents(documents)

        #Crear vectorstore
        print("creando vectorstore")
        vectorstore = self.ceate_vectorstore(chunks)

        return vectorstore
    


    
    




