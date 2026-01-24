from pathlib import Path
from typing import Any
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma

from soporte_tecnico.config import *


class QueryRAG():
    def __init__(self, chroma_path: str = './chroma_db'):
        self.chroma_path = Path(chroma_path)
        self.embedding = OpenAIEmbeddings(model=MODEL_EMBEDDING)
        self.llm = ChatOpenAI(model=MODEL_LLM)
        self.vectorstore = None
        self.retriever = None

        self._load_vectorstore()
    
    def _load_vectorstore(self):
        """Carga vector estore desde disco"""

        if not self.chroma_path.exists():
            print(f"ERROR: no se puede cargar vectorstore, no existe en la ruta: {self.chroma_path}")
            return
        
        self.vectorstore = Chroma(
            collection_name="openai_knowledge",
            embedding_function=self.embedding,
            persist_directory=str(self.chroma_path)
        )

        self.retriever = self.vectorstore.as_retriever(
            search_type = "mmr",
            kwargs = {'k':5, 'fetch_k':20,'lambda_mult':0.75}
        )

        print("Cargado correctamente vectorstore")

    def buscar(self, consulta: str) -> dict[str, Any]:
        """Generar consulta al llm con datos del reitriever"""

        if not self.retriever:
            return {
                "respuesta": "El sistem RAG no esta diponible",
                "filename": [],
                "page":[]
            }
        
        documents = self.retriever.invoke(consulta)

        if not documents:
            return {
                "respuesta": "No existen documentos relevantes sobre esta consulta",
                "filename": [],
                "page":[]
            }
        
        #Extraer contexto y metadata

        contexto_partes = []
        filenames = []
        pages = []

        for doc in documents:
            doc.page_content


        