
from app.agents.planner_agent import plan_research
from app.rag.pipeline import run_rag

async def research(topic):
    try:
        steps = plan_research(topic)
        insights = []
        for step in steps:
            result = await run_rag(step)
            insights.append(result)
        
        return {
            "research": insights,
            "topic": topic,
            "success": True
        }
    except Exception as e:
        return {
            "research": f"Error during research: {str(e)}",
            "topic": topic,
            "success": False
        }
