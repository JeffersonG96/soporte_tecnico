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




def clarify_node(state: MyState):

    state['respuesta'] ="Ejecutando clarify_node"
    return state