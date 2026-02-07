from soporte_tecnico.graph.state import MyState

def support_node(state: MyState):
    state['respuesta'] = "Ejecutando support_node"
    
    return state