from soporte_tecnico.rag.query_rag import QueryRAG
from soporte_tecnico.config import *

def main():
    consulta  = QueryRAG(chroma_path=CHROMA_PATH)

    resultado = consulta.retriever.invoke("Ques es python")

    print(resultado)

if __name__ == "__main__":
    main()