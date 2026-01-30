from soporte_tecnico.graph.graph_builder import GraphBuilder
import asyncio


async def main():
    resp = GraphBuilder()

    # categoria = resp.clasificar_intencion({"consulta": "Como cuento los tokens?"})
    categoria = await resp.ejecutar_rag({"consulta": "Como cuento los tokens de openai?"})

    print(categoria)

if __name__ == "__main__":
    asyncio.run(main())