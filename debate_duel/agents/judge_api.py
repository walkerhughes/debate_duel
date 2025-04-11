from fastapi import FastAPI, HTTPException

from debate_duel.shared.schemas import JudgeRequest, JudgeResponse
from debate_duel.agents.judge import JudgeAgent


app = FastAPI()
judge_agent = JudgeAgent()


@app.post("/judge", response_model=JudgeResponse)
async def judge_debate(request: JudgeRequest) -> JudgeResponse:
    """
    Judge a debate round based on the provided topic and arguments.
    
    Returns:
        A JudgeResponse with the winner and justification.
    """
    try:
        return judge_agent.judge_debate(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error judging debate: {str(e)}") 