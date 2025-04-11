from openai import OpenAI
from typing import List

from debate_duel.settings.constants import OPENAI_MODEL, OPENAI_CLIENT
from debate_duel.shared.schemas import ArgumentRequest, Turn, Stance


class SwarmAgent:
    def __init__(self):
        self.client = OPENAI_CLIENT
    
    def generate_argument(self, request: ArgumentRequest) -> str:
        """
        Generate an argument for the given topic based on the debate history.
        
        Args:
            request: The request containing topic, stance, and debate history
            
        Returns:
            Generated argument as a string
        """
        topic = request.topic
        stance = request.stance
        history = request.history
        
        # Construct prompt based on stance and history
        prompt = self._build_prompt(topic, stance, history)
        
        # Call the OpenAI API
        response = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": self._get_system_prompt(stance)},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        return response.choices[0].message.content
    
    def _get_system_prompt(self, stance: Stance) -> str:
        """
        Get the system prompt for the specified stance.
        """
        if stance == Stance.PRO:
            return (
                "You are a Pro-side debate agent. Your goal is to persuasively argue in favor of the given topic. "
                "Use logical reasoning, evidence, and strong rhetoric to make your case. "
                "Address counterarguments from the opposition and highlight flaws in their reasoning."
            )
        else:
            return (
                "You are a Con-side debate agent. Your goal is to persuasively argue against the given topic. "
                "Use logical reasoning, evidence, and strong rhetoric to make your case. "
                "Address counterarguments from the opposition and highlight flaws in their reasoning."
            )
    
    def _build_prompt(self, topic: str, stance: Stance, history: List[Turn]) -> str:
        """
        Build the prompt for the LLM based on the debate history.
        """
        prompt = f"Topic: {topic}\n\n"
        
        if not history:
            prompt += f"You are arguing {'for' if stance == Stance.PRO else 'against'} this topic. This is the first round of the debate. "
            prompt += "Make a strong opening argument.\n"
        else:
            prompt += "Debate history:\n\n"
            
            for i, turn in enumerate(history):
                prompt += f"Round {i+1}:\n"
                prompt += f"Pro: {turn.pro_argument}\n\n"
                prompt += f"Con: {turn.con_argument}\n\n"
                
                if turn.judge_decision:
                    prompt += f"Judge: Winner: {turn.judge_decision.winner}\n"
                    prompt += f"Justification: {turn.judge_decision.justification}\n\n"
            
            prompt += f"\nYou are arguing {'for' if stance == Stance.PRO else 'against'} this topic. "
            prompt += "Based on the debate history, provide your next argument. "
            prompt += "Focus on rebutting your opponent's points and strengthening your position.\n"
        
        return prompt 