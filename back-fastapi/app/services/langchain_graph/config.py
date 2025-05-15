
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

_llm = None

def generateLLmIstance():
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
    return _llm


