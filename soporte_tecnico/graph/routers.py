from soporte_tecnico.graph.state import MyState

class PolicyRouter:
    def __init__(self, rag_threshold: float = 0.65, min_good_docs: int = 2):
        self.rag_thresshold = rag_threshold
        self.min_good_docs = min_good_docs

    def __call__(self, state: MyState) -> str:
        intent = state.get('intent', 'desconocido')
        best_score = state.get('best_score')
        scores = state.get('scores_rag', [])

        ok_rag = best_score <= 0.65
        good_docs = sum(1 for s in scores if s <= self.rag_thresshold)
        evidence = ok_rag and good_docs >= self.min_good_docs

        state.setdefault("debug", {})
        state["debug"]["policy"] = {"intent": intent, "best_score": best_score, "good_docs": good_docs, "evidence": evidence}

        if intent == "consulta_documentacion":
                return "rag_node" if evidence else "clarify_node"
            
        if intent in ("diagnostico]_soporte", "procedimiento_configuracion"):
                return "support_node"
            
        if intent in ("saludo", "conversacion_general"):
                return "chat_node"
            
        return "clarify_node"