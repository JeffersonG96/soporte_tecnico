from pathlib import Path
from typing import Any
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document


from soporte_tecnico.config import *


class QueryRAG():
    def __init__(self, chroma_path: str = './chroma_db'):
        self.chroma_path = Path(chroma_path)
        self.embedding = OpenAIEmbeddings(model=MODEL_EMBEDDING)
        self.llm = ChatOpenAI(model=MODEL_LLM, temperature=0.1)
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
            search_type = "similarity",
            kwargs = {'k':6}
        )

        print("Cargado correctamente vectorstore")

    async def buscar(self, consulta: str) -> dict[str, Any]:
        """Generar consulta al llm con datos del reitriever"""

        if not self.retriever:
            return {
                "respuesta": "El sistem RAG no esta diponible",
                "filename": [],
                "page":[],
            }
        
        documents = await self.retriever.ainvoke(consulta)

        if not documents:
            return {
                "respuesta": "No existen documentos relevantes sobre esta consulta",
                "filename": [],
                "page":[],
            }
        # self._update_score_vectorstore(consulta, documents)
        #Extraer contexto y metadata
        contexto_partes = []
        filenames = []
        pages = []
        scores = []

        for i, doc in enumerate(documents):
            contexto = doc.page_content.strip()
            if contexto:
                contexto_partes.append(contexto)

                #Extrear nombre de archivos
                filename = doc.metadata.get('filename')
                if filename:
                    filenames.append(filename)
                
                page = doc.metadata.get('page_label')
                if page:
                    pages.append(page)
                
            if not contexto:
                return {
                    "respuesta": "No existe page_content en los documentos",
                    "filename": filename,
                    "page": page,
                }
        
        contexto_unido = "\n\n".join(contexto_partes)
        respuesta = await self._generar_respuesta(consulta, contexto_unido)

        return {
            "respuesta": respuesta,
            "filename": set(filenames),
            "page": set(pages),
        } 
    

    async def _generar_respuesta(self, consulta: str, contexto: str) -> str:
        """Generar respuesta con LLM"""
        prompt = ChatPromptTemplate.from_template(
        f"""
        Eres un experto en RETREIVER  que generar una respuesta coherente con la base de de conocimiento.
        Instrucciones:
        - Genera una respuesta útil.
        - Si no ha contexto suficiente, dilo claramente
        - No inventes información que no esta en el contexto
        - Si el contexto no tiene sentido con la pregunta, dilo claramente

        Contexto de la base de conocimientos: {contexto}

        Pregunta del usuario: {consulta}                                                          
        """)

        try:
            respuesta = self.llm.invoke(prompt.format(consulta=consulta, contexto=contexto))
            return respuesta.content.strip()
        except Exception as e:
            return "LLM no disponible, no se puede procesar la consulta con el contexto"
             
    def get_score_vectorstore(self, consulta: str) -> list[float]:
        
        scored = self.vectorstore.similarity_search_with_score(query=consulta, k=6) if self.vectorstore else []
        scores = [float(s) for _, s in scored]

        return scores







        