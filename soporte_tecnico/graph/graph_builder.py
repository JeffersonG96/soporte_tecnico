from soporte_tecnico.config import *
from soporte_tecnico.rag.query_rag import QueryRAG
from soporte_tecnico.graph.state import MyState
from soporte_tecnico.graph.routers import PolicyRouter
from soporte_tecnico.rag.setup_rag import SetupRAG
from langgraph.graph import START, END, StateGraph

router = PolicyRouter()
score = QueryRAG(chroma_path=CHROMA_PATH)
setup_rag = SetupRAG(docs_path=DOCS_PATH, chroma_path=CHROMA_PATH)

builder = StateGraph(MyState)

builder.add_node("score_node", score.get_score_vectorstore)
builder.add_node("intent", router)

#define workflow
builder.add_edge(START, "score_node")
builder.add_edge("score_node", "intent")
builder.add_edge("intent", END)

graph = builder.compile()




    

