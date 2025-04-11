"""
Researcher agent that gathers information on key debate points
"""
from typing import Dict, List
from debate_duel.settings.constants import OPENAI_CLIENT, OPENAI_MODEL


class ResearcherAgent:
    """
    Agent that researches information on key points for the debate argument.
    """
    
    def __init__(self):
        """Initialize the researcher agent"""
        self.client = OPENAI_CLIENT
    
    def research_points(self, topic: str, points: List[str]) -> Dict[str, str]:
        """
        Research information related to the key points for the debate argument.
        
        Args:
            topic: The debate topic
            points: List of key points to research
            
        Returns:
            Dictionary mapping each point to relevant information
        """
        system_prompt = self._get_system_prompt()
        
        research_results = {}
        
        # Research each point individually
        for point in points:
            user_prompt = self._build_prompt(topic, point)
            
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            research_results[point] = response.choices[0].message.content
        
        return research_results
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the researcher agent"""
        return """
        You are a debate research specialist. Your role is to provide accurate, relevant, and 
        comprehensive information on specific debate points. Focus on facts, statistics, 
        historical examples, and logical principles that can strengthen an argument.
        
        For each research point:
        1. Provide factual information relevant to the point
        2. Include specific examples or evidence when applicable
        3. Consider both supportive and opposing perspectives
        4. Highlight any nuances or complexities
        
        Be concise but thorough. Your research will be used to build a persuasive debate argument.
        """
    
    def _build_prompt(self, topic: str, point: str) -> str:
        """Build the prompt for researching a specific point"""
        prompt = f"Topic: {topic}\n\n"
        prompt += f"Research point: {point}\n\n"
        prompt += "Please provide relevant information, facts, examples, and logical principles related to this point."
        prompt += " The information will be used to build a persuasive debate argument."
        
        return prompt 