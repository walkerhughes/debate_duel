"""
Planner agent that analyzes the debate and identifies key areas to address
"""
from typing import Dict, List, Any
from debate_duel.shared.schemas import Stance, Turn
from debate_duel.settings.constants import OPENAI_CLIENT, OPENAI_MODEL


class PlannerAgent:
    """
    Agent that analyzes the debate history and identifies key areas to address
    in the next argument.
    """
    
    def __init__(self):
        """Initialize the planner agent"""
        self.client = OPENAI_CLIENT
    
    def create_plan(self, topic: str, stance: Stance, history: List[Turn]) -> Dict[str, Any]:
        """
        Create a plan for the debate argument by analyzing the debate history
        and identifying key areas to address.
        
        Args:
            topic: The debate topic
            stance: PRO or CON stance
            history: List of previous debate turns
            
        Returns:
            A plan dictionary with key areas to address
        """
        system_prompt = self._get_system_prompt()
        user_prompt = self._build_prompt(topic, stance, history)
        
        response = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        # Parse the response into a structured plan
        import json
        plan = json.loads(response.choices[0].message.content)
        
        return plan
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the planner agent"""
        return """
        You are a debate planning specialist. Your role is to analyze the debate topic and history,
        then identify key areas that need to be addressed in the next argument.
        
        Your response should be a well-structured JSON object containing:
        1. "overall_approach": A one-sentence summary of the general approach
        2. "points": A list of 3-5 key points that should be addressed
        3. "opponent_weaknesses": A list of weaknesses in the opponent's arguments to exploit
        4. "anticipated_counterarguments": Potential counter-arguments the opponent might make
        
        Be strategic and analytical. Focus on identifying the most important areas that will
        strengthen your position and weaken the opponent's position.
        """
    
    def _build_prompt(self, topic: str, stance: Stance, history: List[Turn]) -> str:
        """Build the prompt for the planner agent"""
        prompt = f"Topic: {topic}\n\n"
        prompt += f"Stance: {'PRO (supporting)' if stance == Stance.PRO else 'CON (opposing)'}\n\n"
        
        if not history:
            prompt += "This is the first round of the debate. There is no history yet.\n\n"
            prompt += "Please create a strategic plan for an opening argument that establishes a strong position.\n"
        else:
            prompt += "Debate history:\n\n"
            
            for i, turn in enumerate(history):
                prompt += f"Round {i+1}:\n"
                prompt += f"PRO: {turn.pro_argument}\n\n"
                prompt += f"CON: {turn.con_argument}\n\n"
                
                if turn.judge_decision:
                    prompt += f"Judge: Winner: {turn.judge_decision.winner}\n"
                    prompt += f"Justification: {turn.judge_decision.justification}\n\n"
            
            prompt += "\nPlease create a strategic plan for the next argument that addresses the current state of the debate.\n"
            prompt += "Consider the opponent's arguments, refute their points, and strengthen your position.\n"
        
        return prompt 