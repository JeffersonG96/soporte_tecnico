from typing import Annotated, List, Any, Optional
from typing_extensions import TypedDict
from operator import add
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages

class MyState(TypedDict):
    """Crear la estructura del estado"""
    messages: Annotated[List[AnyMessage], add_messages]
    intent: str
    intent_confidence: float
    missing_fields: list[str]
    user_query: str
    debug: dict[str, Any] = {}
    best_score: float
    scores_rag: list
    respuesta: str

    slots: dict[str, List[str]]
    updates: list[str]
    clarify: dict[str, Any]
    clarify_attempts: int
    
    categoria: str | None
    requiere_clasificacion: bool
    fuentes: Optional[list]
    page: Optional[list]
    resumen:str
    historial: Annotated[List[AnyMessage], add_messages]
