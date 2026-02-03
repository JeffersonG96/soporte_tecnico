from soporte_tecnico.nodes.detect_intent import detect_intent_node
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from soporte_tecnico.config import *
import asyncio

async def main():
    llm = ChatOpenAI(model=MODEL_LLM, temperature=0)

    messages = [
    SystemMessage(content="Eres un asistente de soporte técnico."),
    HumanMessage(content="Hola"),
    AIMessage(content="Hola, ¿en qué puedo ayudarte?"),
    HumanMessage(content="cual es la version del firmware"),
    ]

    resp = await detect_intent_node({"messages": messages},llm=llm)
    print(resp)


if __name__ == "__main__":
    asyncio.run(main())