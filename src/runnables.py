from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI

def make_openai(model: str = "gpt-4o-mini", temperature: float = 0.0):
    llm = ChatOpenAI(model=model, temperature=temperature)
    def run(prompt: str) -> str:
        return llm.invoke(prompt).content
    return run

def make_mistral(model: str = "mistral-7b", temperature: float = 0.0):
    llm = ChatMistralAI(model=model, temperature=temperature)
    def run(prompt: str) -> str:
        return llm.invoke(prompt).content
    return run
