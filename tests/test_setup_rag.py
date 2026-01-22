from soporte_tecnico.rag.setup_rag import SetupRAG
from soporte_tecnico.config import *

def main():

    loadder = SetupRAG(docs_path=DOCS_PATH, chroma_path=CHROMA_PATH)

    print(len(loadder.load_documents()))


if __name__ == "__main__":
    main()