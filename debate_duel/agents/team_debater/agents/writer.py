"""
Writer agent that crafts the final debate argument
"""
from typing import Dict, List, Any
from debate_duel.shared.schemas import Stance, Turn
from debate_duel.settings.constants import OPENAI_CLIENT, OPENAI_MODEL


class WriterAgent:
    """
    Agent that crafts the final debate argument based on the plan, research, 
    strategy, and debate history.
    """
    
    def __init__(self):
        """Initialize the writer agent"""
        self.client = OPENAI_CLIENT
    
    def write_argument(
        self,
        topic: str,
        stance: Stance,
        history: List[Turn],
        plan: Dict[str, Any],
        research_results: Dict[str, str],
        strategy: Dict[str, Any]
    ) -> str:
        """
        Write the final debate argument.
        
        Args:
            topic: The debate topic
            stance: PRO or CON stance
            history: List of previous debate turns
            plan: The debate plan created by the planner
            research_results: Research information on key points
            strategy: The strategy developed by the strategist
            
        Returns:
            The final debate argument as a string
        """
        system_prompt = self._get_system_prompt()
        user_prompt = self._build_prompt(topic, stance, history, plan, research_results, strategy)
        
        response = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the writer agent"""
        return """
        You are a skilled debate writer. Your role is to craft a persuasive, eloquent, and 
        powerful debate argument based on the provided plan, research, and strategy.
        
        Your argument should:
        1. Follow the suggested structure and strategic approach
        2. Integrate key points and evidence effectively
        3. Use rhetorical techniques for maximum persuasive impact
        4. Address anticipated counterarguments
        5. Maintain a confident, authoritative tone
        
        Be articulate, precise, and persuasive. Focus on crafting an argument that will convince
        both the opponent and any judges or audience.
        """
    
    def _build_prompt(
        self,
        topic: str,
        stance: Stance,
        history: List[Turn],
        plan: Dict[str, Any],
        research_results: Dict[str, str],
        strategy: Dict[str, Any]
    ) -> str:
        """Build the prompt for the writer agent"""
        prompt = f"Topic: {topic}\n\n"
        prompt += f"Stance: {'PRO (supporting)' if stance == Stance.PRO else 'CON (opposing)'}\n\n"
        
        # Include debate plan summary
        prompt += "DEBATE PLAN:\n"
        prompt += f"Overall Approach: {plan.get('overall_approach', 'N/A')}\n"
        if 'points' in plan:
            prompt += "Key Points:\n"
            for i, point in enumerate(plan['points']):
                prompt += f"  {i+1}. {point}\n"
        
        # Include strategy summary
        prompt += "\nSTRATEGY:\n"
        if 'key_messaging' in strategy:
            prompt += "Key Messaging:\n"
            for i, msg in enumerate(strategy['key_messaging']):
                prompt += f"  {i+1}. {msg}\n"
        
        if 'argument_structure' in strategy:
            prompt += f"\nArgument Structure: {strategy['argument_structure']}\n"
        
        # Include abbreviated research results
        prompt += "\nRESEARCH (Key Information):\n"
        for point, info in research_results.items():
            prompt += f"\n[{point}] - Key insights available to incorporate\n"
        
        # Include brief debate history if available
        if history:
            last_turn = history[-1]
            opponent_argument = last_turn.con_argument if stance == Stance.PRO else last_turn.pro_argument
            prompt += "\nLAST OPPONENT ARGUMENT:\n"
            prompt += f"{opponent_argument[:300]}...\n"
        
        prompt += "\nBased on all the provided information, please write a compelling and persuasive debate argument.\n"
        prompt += "Focus on implementing the strategic approach while addressing key points with supporting evidence.\n"
        
        return prompt 