from typing import Annotated, List, Any, Optional, TypedDict
from operator import add
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages

class RagState(TypedDict):
    consulta: str
    respuesta: str
    categoria: str | None
    score_rag: list
    requiere_clasificacion: bool
    fuentes: Optional[list]
    page: Optional[list]
    resumen:str
    historial: Annotated[List[AnyMessage], add_messages]
