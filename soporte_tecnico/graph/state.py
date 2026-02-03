from typing import Annotated, List, Any, Optional, TypedDict
from operator import add
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages

class MyState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    intent: str
    intent_confidence: float
    missing_fields: list[str]
    user_query: str
    debug: dict[str, Any] = {}

    respuesta: str
    categoria: str | None
    best_score: list
    requiere_clasificacion: bool
    fuentes: Optional[list]
    page: Optional[list]
    resumen:str
    historial: Annotated[List[AnyMessage], add_messages]
