import uvicorn
import os

def main():
    """
    Run the arena API service.
    """
    port = int(os.environ.get("PORT", "8000"))
    host = os.environ.get("HOST", "0.0.0.0")
    
    uvicorn.run(
        "debate_duel.arena.api:app",
        host=host,
        port=port,
        log_level="info",
        reload=True
    )


if __name__ == "__main__":
    main() 