import httpx
import asyncio
from typing import List

from debate_duel.settings.constants import SERVICE_URLS
from debate_duel.shared.schemas import (
    TopicRequest, 
    ArgumentRequest, 
    Turn, 
    JudgeRequest,
    JudgeResponse,
    Stance,
    Winner,
    DebateResult
)
from debate_duel.arena.elo import EloEngine


class DebateOrchestrator:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=60.0)
        self.elo_engine = EloEngine()
    
    async def run_debate(self, topic_request: TopicRequest) -> DebateResult:
        """
        Run a complete debate with the specified number of turns.
        
        Args:
            topic_request: The topic and number of turns for the debate
            
        Returns:
            A DebateResult with the full history and ELO trajectory
        """
        topic = topic_request.topic
        num_turns = topic_request.num_turns
        turns: List[Turn] = []
        
        # Record initial ELO
        initial_elo = self.elo_engine.ratings.copy()
        
        for turn_idx in range(num_turns):
            # Get arguments from both swarms
            pro_argument, con_argument = await asyncio.gather(
                self._get_argument(topic, Stance.PRO, turns),
                self._get_argument(topic, Stance.CON, turns)
            )
            
            # Get judge's decision
            judge_response = await self._get_judge_decision(topic, pro_argument, con_argument)
            
            # Create turn record
            turn = Turn(
                pro_argument=pro_argument,
                con_argument=con_argument,
                judge_decision=judge_response
            )
            turns.append(turn)
            
            # Update ELO ratings
            self.elo_engine.update(judge_response.winner)
        
        # Determine final winner based on final ELO scores
        if self.elo_engine.ratings["pro"] > self.elo_engine.ratings["con"]:
            final_winner = Winner.PRO
        elif self.elo_engine.ratings["con"] > self.elo_engine.ratings["pro"]:
            final_winner = Winner.CON
        else:
            final_winner = Winner.TIE
        
        # Create final result
        result = DebateResult(
            topic=topic,
            turns=turns,
            final_winner=final_winner,
            initial_elo=initial_elo,
            final_elo=self.elo_engine.ratings,
            elo_trajectory=self.elo_engine.get_trajectory()
        )
        
        return result
    
    async def _get_argument(self, topic: str, stance: Stance, history: List[Turn]) -> str:
        """
        Request an argument from a swarm agent.
        """
        service_key = "swarm_a" if stance == Stance.PRO else "swarm_b"
        url = f"{SERVICE_URLS[service_key]}/generate_argument"
        
        request = ArgumentRequest(
            topic=topic,
            stance=stance,
            history=history
        )
        
        response = await self.client.post(url, json=request.model_dump())
        response.raise_for_status()
        
        return response.json()["content"]
    
    async def _get_judge_decision(self, topic: str, pro_argument: str, con_argument: str) -> JudgeResponse:
        """
        Request a judgment from the judge agent.
        """
        url = f"{SERVICE_URLS['judge']}/judge"
        
        request = JudgeRequest(
            topic=topic,
            pro_argument=pro_argument,
            con_argument=con_argument
        )
        
        response = await self.client.post(url, json=request.model_dump())
        response.raise_for_status()
        
        return JudgeResponse(**response.json())
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose() 