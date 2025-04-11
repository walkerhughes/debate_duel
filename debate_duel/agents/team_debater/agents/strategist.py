"""
Strategist agent that determines effective arguments and structure
"""
from typing import Dict, List, Any
from debate_duel.shared.schemas import Stance, Turn
from debate_duel.settings.constants import OPENAI_CLIENT, OPENAI_MODEL


class StrategistAgent:
    """
    Agent that develops a strategic approach to the debate argument based on
    the plan, research, and debate history.
    """
    
    def __init__(self):
        """Initialize the strategist agent"""
        self.client = OPENAI_CLIENT
    
    def develop_strategy(
        self,
        topic: str,
        stance: Stance,
        history: List[Turn],
        plan: Dict[str, Any],
        research_results: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Develop a strategic approach for the debate argument.
        
        Args:
            topic: The debate topic
            stance: PRO or CON stance
            history: List of previous debate turns
            plan: The debate plan created by the planner
            research_results: Research information on key points
            
        Returns:
            A strategy dictionary with the approach and structure for the argument
        """
        system_prompt = self._get_system_prompt()
        user_prompt = self._build_prompt(topic, stance, history, plan, research_results)
        
        response = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.5
        )
        
        # Parse the response into a structured strategy
        import json
        strategy = json.loads(response.choices[0].message.content)
        
        return strategy
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the strategist agent"""
        return """
        You are a debate strategy specialist. Your role is to develop an effective strategic approach
        for a debate argument based on the plan, research, and debate history.
        
        Your response should be a well-structured JSON object containing:
        1. "key_messaging": A list of 3-4 key messages to emphasize
        2. "argument_structure": An outline of how to structure the argument
        3. "rhetorical_techniques": A list of specific rhetorical techniques to employ
        4. "rebuttal_strategies": How to address anticipated counterarguments
        5. "evidence_prioritization": Which evidence should be emphasized most
        
        Be strategic and persuasive. Focus on creating a compelling, well-structured argument
        that will be effective in the debate context.
        """
    
    def _build_prompt(
        self,
        topic: str,
        stance: Stance,
        history: List[Turn],
        plan: Dict[str, Any],
        research_results: Dict[str, str]
    ) -> str:
        """Build the prompt for the strategist agent"""
        prompt = f"Topic: {topic}\n\n"
        prompt += f"Stance: {'PRO (supporting)' if stance == Stance.PRO else 'CON (opposing)'}\n\n"
        
        # Include debate plan
        prompt += "DEBATE PLAN:\n"
        for key, value in plan.items():
            if isinstance(value, list):
                prompt += f"\n{key.upper()}:\n"
                for i, item in enumerate(value):
                    prompt += f"  {i+1}. {item}\n"
            else:
                prompt += f"\n{key.upper()}: {value}\n"
        
        # Include research results
        prompt += "\nRESEARCH RESULTS:\n"
        for point, info in research_results.items():
            prompt += f"\n[{point}]\n{info}\n"
        
        # Include debate history summary if available
        if history:
            prompt += "\nDEBATE HISTORY SUMMARY:\n"
            for i, turn in enumerate(history):
                prompt += f"Round {i+1} Winner: {turn.judge_decision.winner if turn.judge_decision else 'N/A'}\n"
        
        prompt += "\nPlease develop a strategic approach for this debate argument.\n"
        prompt += "Consider the plan, research, and debate history to create an effective strategy.\n"
        
        return prompt 