"""
Main module for the team debater API service
"""
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from debate_duel.shared.schemas import ArgumentRequest
from debate_duel.agents.team_debater.manager import DebateAgentManager

# Initialize the app
app = FastAPI(title="Team Debate Agent API")

# Initialize the team debater manager
team_debater = DebateAgentManager(verbose=os.getenv("DEBUG", "False").lower() == "true")


@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agent": "team_debater"}


@app.post("/generate")
async def generate_argument(request: ArgumentRequest):
    """
    Generate a debate argument
    
    Args:
        request: ArgumentRequest containing topic, stance, and debate history
        
    Returns:
        The generated argument
    """
    try:
        argument = team_debater.generate_argument(request)
        return {"argument": argument}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate argument: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(app, host=host, port=port) 