import os 
from dotenv import load_dotenv

load_dotenv()
if os.getenv("OPENAI_API_KEY"):
    print("cargado correctamente")



CHROMA_PATH="D:\\Cursos\\Agentes\\soporte_tecnico\\soporte_tecnico\\data\\chroma_db"
DOCS_PATH = "D:\\Cursos\\Agentes\\soporte_tecnico\\soporte_tecnico\\data\\docs"
MODEL_EMBEDDING = "text-embedding-3-large"
MODEL_LLM = "4o-gpt-mini"