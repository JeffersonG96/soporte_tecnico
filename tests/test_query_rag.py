import asyncio
from soporte_tecnico.rag.query_rag import QueryRAG
from soporte_tecnico.config import *

async def main():
    consulta  = QueryRAG(chroma_path=CHROMA_PATH)

    resultado = await consulta.buscar(consulta="define python")
    # resultado = consulta.test("que es python")
    # resultado = consulta.retriever.invoke("Como cuentos tokens ?")

    print(resultado)
    # print(f"\n\n {len(resultado)}")

if __name__ == "__main__":
    asyncio.run(main())