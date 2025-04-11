import uvicorn
import os

def main():
    """
    Run the con swarm agent API service.
    """
    port = int(os.environ.get("PORT", "8002"))
    host = os.environ.get("HOST", "0.0.0.0")
    
    uvicorn.run(
        "debate_duel.agents.swarm_api:app",
        host=host,
        port=port,
        log_level="info",
        reload=True
    )


if __name__ == "__main__":
    main() 