from typing import Optional, Literal
from pydantic import BaseModel, Field
from soporte_tecnico.graph.state import MyState

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate

Intent = Literal[
    "diagnostico_soporte",
    "procedimiento_configuracion",
    "consulta_documentacion",
    "conversacion_general",
    "saludo",
    "desconocido",
]

#Catálogo de slots
SLOT_CATALOG: dict[Intent, list[str]] = {
    "diagnostico_soporte": ["modelo_equipo", "sintoma", "operador", "apn"],
    "procedimeinto_configuracion": ["modelo_equipo", "objetivo_config", "parametros_conocidos"],
    "consulta_documentacion": ["producto", "tema"],
    "conversacion_general": [],
    "saludo": [],
    "desconocido": []
}

#Campos mínimos por intención 
REQUIRED_BY_INTENT: dict[Intent, list[str]] = {
    "diagnostico_soporte": ["modelo_quipo", "sintoma"],
    "procedimeinto_configuracion": ["modelo_equipo", "objetivo_config"],
    "consulta_documentacion": [],
    "conversacion_general": [],
    "saludo": [],
    "desconocido": []
}

#Salida estructurada con pydantic 
class SlotExtraction(BaseModel):
    modelo_equipo: Optional[str] = None
    sintoma: Optional[str] = None
    operador: Optional[str] = None
    apn: Optional[str] = None
    objetivo_config: Optional[str] = None
    parametros_conocidos: Optional[str] = None
    producto: Optional[str] = None
    tema: Optional[str] = None

    update: list[str] = Field(default_factory=list, description= "Lista de  slots que se actualizan")
    confidence: float = Field(ge=0.0, le=1.0, default=0.7)
    
SLOT_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Eres un extractor de slots para un asistente de soporte técnico.\n"
     "Extrae SOLO la información explícita del último mensaje del usuario.\n"
     "No inventes. Si no aparece, deja el campo como null.\n"
     "Debes respetar el catálogo de slots permitido y actualizar SOLO lo relevante.\n"
     "Incluye en 'updates' los nombres de los campos que detectaste en este turno.\n"
     "Devuelve salida usando el esquema estructurado proporcionado."),
    ("human",
     "Intent actual: {intent}\n"
     "Slots actuales: {current_slots}\n"
     "Slots permitidos para esta intent: {allowed_slots}\n"
     "Campos requeridos (mínimos): {required_slots}\n\n"
     "Último mensaje del usuario:\n"
     "{text}")
])


def _merge_slots(existing: dict, extracted: SlotExtraction, allowed: list[str]) -> dict:
    updated = dict(existing or {})
    extracted_dict = extracted.model_dump()

    # Solo considera slots permitidos y no-vacíos
    for k in allowed:
        val = extracted_dict.get(k)
        if val is not None:
            updated[k] = val
    return updated

def _compute_missing(intent: Intent, slots: dict) -> list[str]:
    required = REQUIRED_BY_INTENT.get(intent, [])
    missing = []
    for r in required:
        if not slots.get(r):
            missing.append(r)
    return missing


class ExtractSlotsNode:
    """Extraer slots del último mensaje"""
    def __init__(self, llm):
        self.chain = SLOT_PROMPT | llm.with_structured_output(SlotExtraction)

    async def __call__(self, state: MyState) -> MyState:
       intent_raw = state.get("intent", "desconocido")
       intent = str(intent_raw).strip().lower()
       text = state.get("user_query")

       current_slots = state.get("slots", {}) or {}
       allowed_slots = SLOT_CATALOG.get(intent, SLOT_CATALOG["desconocido"])
       required_slots = REQUIRED_BY_INTENT.get(intent, [])

       result: SlotExtraction = await self.chain.ainvoke({
           "intent": intent,
           "current_slots": current_slots,
           "allowed_slots": allowed_slots,
           "required_slots": required_slots,
           "text": text
       })

       print("="*80)    
       print(result)

       merged = _merge_slots(current_slots,result,allowed_slots)
       missing = _compute_missing(intent,merged)

       state["slots"] = merged
       state["missing_fields"] = missing

       state.setdefault("debug", {})
       state["debug"]["slots_extraction"] = {
            "intent": intent,
            "allowed_slots": allowed_slots,
            "required_slots": required_slots,
            "updates": result.update,
            "confidence": float(result.confidence),
            "extracted_raw": result.model_dump(),
            "merged_slots": merged,
            "missing_fields": missing,
       }

       return state
