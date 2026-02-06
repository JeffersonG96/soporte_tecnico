from soporte_tecnico.nodes.detect_intent import DetectIntent
from soporte_tecnico.graph.state import MyState
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from soporte_tecnico.config import *
import asyncio

async def main():
    llm = ChatOpenAI(model=MODEL_LLM, temperature=0)
    state = MyState()

    messages = [
    SystemMessage(content="Eres un asistente de soporte técnico."),
    HumanMessage(content="Hola"),
    AIMessage(content="Hola, ¿en qué puedo ayudarte?"),
    HumanMessage(content="hola, cual es la version del firmware"),
    ]
    state['messages'] = messages

    detect = DetectIntent(llm)
    out_state = await detect(state=state)
    
    print(out_state)


if __name__ == "__main__":
    asyncio.run(main())