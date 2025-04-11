import os 
from openai import OpenAI

OPENAI_MODEL = "gpt-4o-mini"
OPENAI_CLIENT = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

DEFAULT_ELO = 1200
ELO_K_FACTOR = 32

SERVICE_URLS = {
    "swarm_a": "http://swarm-a:8000",
    "swarm_b": "http://swarm-b:8000",
    "judge": "http://judge-agent:8000",
}
