
from app.llm.loader import LLMManager

def plan_research(topic):
    llm = LLMManager().get_llm()
    res = llm.invoke(f"Generate 5 research questions about {topic}")
    return res.split("\n")
