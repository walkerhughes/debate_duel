from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

from debate_duel.shared.schemas import TopicRequest, DebateResult
from debate_duel.arena.orchestrator import DebateOrchestrator


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.orchestrator = DebateOrchestrator()
    yield
    await app.state.orchestrator.close()


app = FastAPI(lifespan=lifespan)


@app.post("/debate", response_model=DebateResult)
async def run_debate(topic_request: TopicRequest) -> DebateResult:
    """
    Run a debate between two AI swarms on the given topic.
    
    Returns:
        The complete debate history, ELO trajectory, and final winner.
    """
    try:
        return await app.state.orchestrator.run_debate(topic_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running debate: {str(e)}") 