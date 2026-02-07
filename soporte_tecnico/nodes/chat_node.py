from soporte_tecnico.graph.state import MyState
from soporte_tecnico.config import *
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage


chat_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Eres un asistente útil de soporte técnico.\n"
     "Tu rol es conversar, explicxar conceptos generales y orientar al usuario.\n"
     "No has el diagnostico profundo y tampoco cites documentos.\n"
     "Si la pregunta es ambigua pide una aclaración.\n"
     "Respone de una forma clara, profesional y concisa"
     ),
     ("human", "{question}")
])

def build_chat_node(llm):
    """Nodo para conversación general y saludos"""
    async def chat_node(state: MyState) -> dict:
        question = state.get('user_query')

        if not question:
            state["respuesta"] = "En que puedo ayudarte"
            return state
        
        chain = chat_prompt | llm

        response = await chain.ainvoke({"question": question})

        state["respuesta"] = response.content

        state.setdefault("messages",[])
        state["messages"].append(AIMessage(content=response.content))

        return state
    return chat_node



    
