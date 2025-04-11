from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class Stance(str, Enum):
    PRO = "pro"
    CON = "con"


class Winner(str, Enum):
    PRO = "pro"
    CON = "con"
    TIE = "tie"


class TopicRequest(BaseModel):
    topic: str
    num_turns: int = 3


class ArgumentRequest(BaseModel):
    topic: str
    stance: Stance
    history: List["Turn"] = []


class JudgeRequest(BaseModel):
    topic: str
    pro_argument: str
    con_argument: str


class JudgeResponse(BaseModel):
    winner: Winner
    justification: str


class Turn(BaseModel):
    pro_argument: str
    con_argument: str
    judge_decision: Optional[JudgeResponse] = None


class DebateResult(BaseModel):
    topic: str
    turns: List[Turn]
    final_winner: Winner
    initial_elo: dict
    final_elo: dict
    elo_trajectory: List[dict]


# Resolve forward references
ArgumentRequest.model_rebuild() 