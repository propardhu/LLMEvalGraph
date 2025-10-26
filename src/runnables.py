from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI

def make_openai(model: str = "gpt-4o-mini", temperature: float = 0.0):
    llm = ChatOpenAI(model=model, temperature=temperature)
    def run(prompt: str) -> str:
        return llm.invoke(prompt).content
    return run

MISTRAL_ALIASES = {
    "mistral-7b": "open-mistral-7b",
    "mixtral-8x7b": "open-mixtral-8x7b",
}
def make_mistral(model: str = "open-mistral-7b", temperature: float = 0.0):
    model = MISTRAL_ALIASES.get(model, model)
    llm = ChatMistralAI(model=model, temperature=temperature)
    def run(prompt: str) -> str:
        return llm.invoke(prompt).content
    return run
