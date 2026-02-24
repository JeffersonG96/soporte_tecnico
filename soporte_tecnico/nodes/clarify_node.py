from soporte_tecnico.graph.state import MyState


FIELD_QUESTIONS: dict[str, str] = {
    "tipo_equipo": "¿Qué tipo de equipo es?",
    "modelo_equipo": "¿Cuál es el modelo del equipo?",
    "sintoma": "¿Cuál es el problema?",
    "operador": "¿Qué operador o chip esta usando?",
    "apn": "¿Cuál es el apn configurada actualmente?",
    "objetivo_config": "¿Qué quieres configurar exactamente?",
    "parametros_conocidos": "¿Qué parámetros ya tienes?",
    "producto": "¿Sobre que producto/ducumentación es la consulta?",
    "tema": "¿Cuál es el tema que quieres consultar?"
}


PRIORITY_BY_INTENT: dict[str, list[str]] = {
    "diagnostico_soporte": ["modelo_equipo", "sintoma", "operador", "apn"],
    "procedimiento_configuracion": ["modelo_equipo", "objetivo_config", "parametros_conocidos"],
    "consulta_documentacion": ["producto", "tema"],
}


class ClarifyNode:
    """Si faltan campos mínimos (missing_fields), genera una pregunta, 
    esta sale por state["clarify]"""

    def __init__(self):
        pass

    async def __call__(self, state: MyState) -> MyState:
        intent = state.get("intent", "desconocido")
        slots = state.get("slots", {}) or {}
        missing = state.get("missing_fields", []) or []

        if intent == "desconocido":
            state["clarify"] = {
                "field": "intent_desambiguation",
                "question": (
                    "Para ayudarte de mejor manera dime qué necesitas:\n"
                    "1. Diagnostico de un problema\n"
                    "2. Configuración o procedimiento\n"
                    "3. Consultar documentacion"
                )
            }

            return state
        
        #si no hay missing no preguntar nada 
        if not missing:
            state["clarify"] = {}
            return state
        
        #Preguntar con prioridad segun la intención 
        priority = PRIORITY_BY_INTENT.get(intent, [])
        next_field = None

        



