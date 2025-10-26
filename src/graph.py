from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from prompts import wrap

class State(TypedDict):
    question_ctx: str
    draft: str
    flags: List[str]

def build_graph(runnable):
    def answer_node(s: State) -> State:
        return {"draft": runnable(wrap(s["question_ctx"]))}

    def validate_node(s: State) -> State:
        txt = (s["draft"] or "").lower()
        flags = []
        if "final:" not in txt: flags.append("missing_final")
        if "evidence:" not in txt: flags.append("missing_evidence")
        return {"flags": flags}

    g = StateGraph(State)
    g.add_node("answer", answer_node)
    g.add_node("validate", validate_node)
    g.set_entry_point("answer")
    g.add_edge("answer", "validate")
    g.add_edge("validate", END)
    return g.compile()
