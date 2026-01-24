from soporte_tecnico.rag.setup_rag import SetupRAG
from soporte_tecnico.config import *

def main():

    setup_rag = SetupRAG(docs_path=DOCS_PATH, chroma_path=CHROMA_PATH)

    setup_rag.setup_rag(force_rebuild=True)


if __name__ == "__main__":
    main()