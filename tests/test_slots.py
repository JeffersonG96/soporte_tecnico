from soporte_tecnico.nodes.extract_slots import ExtractSlotsNode
from langchain_openai import ChatOpenAI
from soporte_tecnico.config import MODEL_LLM
import asyncio


async def main():
    llm = ChatOpenAI(model=MODEL_LLM, temperature=0)
    resp = ExtractSlotsNode(llm=llm)

    # categoria = resp.clasificar_intencion({"consulta": "Como cuento los tokens?"})
    categoria = await resp.ejecutar_rag({"consulta": "Como cuento los tokens de openai?"})

    print(categoria)

if __name__ == "__main__":
    asyncio.run(main())