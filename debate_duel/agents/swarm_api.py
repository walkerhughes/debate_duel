from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from debate_duel.shared.schemas import ArgumentRequest
from debate_duel.agents.swarm import SwarmAgent


class ArgumentResponse(BaseModel):
    content: str


app = FastAPI()
swarm_agent = SwarmAgent()


@app.post("/generate_argument", response_model=ArgumentResponse)
async def generate_argument(request: ArgumentRequest) -> ArgumentResponse:
    """
    Generate a debate argument based on the provided topic, stance, and history.
    
    Returns:
        An ArgumentResponse containing the generated argument.
    """
    try:
        argument = swarm_agent.generate_argument(request)
        return ArgumentResponse(content=argument)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating argument: {str(e)}") 