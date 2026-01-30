from langchain_openai import ChatOpenAI
from typing import Any
from langchain_core.prompts import ChatPromptTemplate

from soporte_tecnico.config import *
from soporte_tecnico.rag.query_rag import QueryRAG
from soporte_tecnico.graph.state import RagState

class GraphBuilder():

    def __init__(self):
        self.llm = ChatOpenAI(model=MODEL_LLM, temperature=0)
        self.rag = QueryRAG(chroma_path=CHROMA_PATH)
    
    # *Nodos para graph
    def clasificar_intencion(self, state: RagState) ->dict[str, Any]:
        """Clasifica la inención del usuario"""
        consulta = state.get('consulta')
        print(f"Consulta del usuario: {consulta}")
        if consulta:
            categoria = self._clasificar_prompt(consulta)
            return{
                "categoria": categoria,
                "historial": f"La intención del usuario es: {categoria}"
            }
        else:
            return {
                "categoria": "No existe datos en la consulta para clasificar adecuadamente",
                "historial": "No existe consulta"
            }
        
    def _clasificar_prompt(self, consulta: str) -> str:
        """Prompt para categorizar"""
        prompt = ChatPromptTemplate.from_template(
        f"""
        Eres un experto en identificar intenciones del usurio, responde solamente con estas intenciones: "rag", "general"
        - rag: el sistema dirige automaticamente al sistema RAG
        - general: el sistema respondera preguntas generales

        Consulta del usuario: {consulta}
        """
        )

        try:
            resp = self.llm.invoke(prompt.format(consulta=consulta))
            return resp.content.strip()
        except Exception as e:
            return f"No se puede clasificar la intencion: {e}"
        

    async def ejecutar_rag(self, state: RagState) ->dict[str, Any]:
        resp = await self.rag.buscar(state.get('consulta'))

        return {
            "respuesta": resp['respuesta'],
            "filename": resp['filename'],
            "page": resp["page"],
            "score_rag":resp["score_rag"],
            "historial": f"La conuslta fue: {resp['respuesta']}"
        }
    
    
    
    
