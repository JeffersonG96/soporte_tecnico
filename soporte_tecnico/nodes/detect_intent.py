from typing import Optional, Literal
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from soporte_tecnico.graph.state import MyState


#Intenciones (5 + desconocido)
Intent = Literal[
    "diagnostico_soporte",
    "procedimiento_configuracion",
    "consulta_documentacion",
    "conversacion_general",
    "saludo",
    "desconocido"
]

#Modelo estructurado - runtime
class IntentResult(BaseModel):
    intent: Intent = Field(...,description="Intencion del usuario según el catálago") 
    confidence: float = Field(...,ge=0.0, le=1.0,description="Confianza de 0 al 1, siendo 0 la mas baja: preferir por desconocido")
    why: str = Field(..., min_length=3, max_length=150, description="Razón breve de la intención eligida")
    missing_fields: list[str] = Field(default_factory=list, description="Campos faltantes")


def _last_user_msg(state: MyState) ->str:
    """Extrae el último HumanMenssage del estado"""
    for m in reversed(state.get('messages', [])):
        if isinstance(m, HumanMessage):
            return m.content or ""
    return ""

#prompt para cladificar intención 
INTENT_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "Eres un CLASIFICADOR de intención para un asistente de SOPORTE TÉCNICO.\n"
        "Tu tarea: clasificar la intención del usuario.\n"
        "IMPORTANTE: NO decidas RAG aquí. Solo intención.\n\n"
        "Intenciones:\n"
        "- diagnostico_soporte: reporta problema/error/síntoma y quiere diagnóstico.\n"
        "- procedimiento_configuracion: pide pasos para configurar/instalar/habilitar algo.\n"
        "- consulta_documentacion: requiere respuesta basada en documentación/manual/datos exactos\n"
        "- conversacion_general: explicación conceptual/general sin depender de docs.\n"
        "- saludo: saludo, agradecimiento, confirmación breve.\n"
        "- desconocido: ambiguo o no se puede determinar.\n\n"
        "Si falta información crítica, baja confidence y llena missing_fields "
        "(ej: modelo_equipo, codigo_error, version_firmware, logs, entorno).\n"
        "Responde usando el esquema estructurado proporcionado.",
    ),
    ("human","{text}"),
])

async def detect_intent_node(state: MyState, llm, min_confidence: float = 0.60) -> dict:
    """
    Nodo LangGraph: detecta intención usando structured output.

    Requiere: state['messages'] con al menos un HumanMessage

    Escribe: 
    - intent, intent_confidence, missing_fields, debug.intent (resultado completo)
    """
    
    text = state.get("user_query") or _last_user_msg(state)
    state["user_query"] = text

    #Clasificar con salida estructurada 
    classifier = INTENT_PROMPT | llm.with_structured_output(IntentResult)

    try:
        result: IntentResult  = await classifier.ainvoke({"text": text})
    except Exception as e:
        print(f"ERROR {e}")
        state["intent"] = "desconocido"
        state["intent_confidence"] = 0.0
        state["missing_fields"] = ["detalle_pregunta"]
        state.setdefault("debug", {})
        state["debug"]["intent"] = {"error": str(e), "input": text[:400]}
        return state
    
    intent = result.intent
    conf = float(result.confidence)

    if conf < min_confidence:
        intent = "desconocido"
    
    state["intent"] = intent
    state["intent_confidence"] = conf
    state["missing_fields"] = result.missing_fields[:6]

    state.setdefault("debug", {})
    state["debug"]["intent"] = result.model_dump()
    
    return state



            
