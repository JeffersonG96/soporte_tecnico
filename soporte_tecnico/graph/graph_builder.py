from soporte_tecnico.config import *
from soporte_tecnico.rag.query_rag import QueryRAG
from soporte_tecnico.graph.state import MyState
from soporte_tecnico.graph.routers import PolicyRouter
from soporte_tecnico.rag.setup_rag import SetupRAG
from soporte_tecnico.nodes.detect_intent import DetectIntent
from soporte_tecnico.nodes import clarify_node, rag_node, support_node
from soporte_tecnico.nodes.chat_node import build_chat_node
from soporte_tecnico.nodes.extract_slots import ExtractSlotsNode

from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, StateGraph

llm=ChatOpenAI(model=MODEL_LLM, temperature=0)

router = PolicyRouter()
score = QueryRAG(chroma_path=CHROMA_PATH)
intent = DetectIntent(llm=llm)
setup_rag = SetupRAG(docs_path=DOCS_PATH, chroma_path=CHROMA_PATH)
slots = ExtractSlotsNode(llm=llm)

# nodos
chat_node = build_chat_node(llm=llm)

builder = StateGraph(MyState)

builder.add_node("score_node", score.get_score_vectorstore)
builder.add_node("intent", intent)
builder.add_node("rag_node",rag_node.rag_node)
builder.add_node("chat_node", chat_node)
builder.add_node("clarify_node", clarify_node.clarify_node)
builder.add_node("support_node",support_node.support_node)
builder.add_node("slot",slots)

#define workflow
builder.add_edge(START, "score_node")
builder.add_edge("score_node", "intent")
builder.add_edge("intent","slot")
builder.add_conditional_edges("slot",router,{
    "rag_node":"rag_node",
    "support_node": "support_node",
    "chat_node":"chat_node",
    "clarify_node":"clarify_node"
})

builder.add_edge("clarify_node", "slot")


graph = builder.compile()

