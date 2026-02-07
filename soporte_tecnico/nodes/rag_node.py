from soporte_tecnico.graph.state import MyState

def rag_node(state: MyState):
    state['respuesta'] = "Ejecutando rag_node"
    
    return state