"""
Verifier agent that checks the debate argument for soundness and identifies weaknesses
"""
from typing import List
from debate_duel.shared.schemas import Stance, Turn
from debate_duel.settings.constants import OPENAI_CLIENT, OPENAI_MODEL


class VerifierAgent:
    """
    Agent that verifies the debate argument for logical soundness, factual accuracy,
    and persuasive strength, then suggests improvements.
    """
    
    def __init__(self):
        """Initialize the verifier agent"""
        self.client = OPENAI_CLIENT
    
    def verify_argument(
        self,
        topic: str,
        stance: Stance,
        history: List[Turn],
        argument: str
    ) -> str:
        """
        Verify the debate argument and make improvements.
        
        Args:
            topic: The debate topic
            stance: PRO or CON stance
            history: List of previous debate turns
            argument: The draft debate argument
            
        Returns:
            The improved debate argument
        """
        system_prompt = self._get_system_prompt()
        user_prompt = self._build_prompt(topic, stance, history, argument)
        
        response = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.4,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the verifier agent"""
        return """
        You are a debate verification specialist. Your role is to review debate arguments
        for logical soundness, factual accuracy, and persuasive strength, then suggest improvements.
        
        When verifying an argument:
        1. Check for logical fallacies or weaknesses
        2. Verify that claims are properly supported
        3. Ensure the argument addresses anticipated counterarguments
        4. Confirm the argument maintains a strong rhetorical structure
        5. Make specific improvements to strengthen the argument
        
        If the argument is generally strong, make minor refinements to enhance its impact.
        If there are significant issues, rewrite relevant sections while maintaining the
        original intent and structure.
        
        Return the improved version of the argument.
        """
    
    def _build_prompt(
        self,
        topic: str,
        stance: Stance,
        history: List[Turn],
        argument: str
    ) -> str:
        """Build the prompt for the verifier agent"""
        prompt = f"Topic: {topic}\n\n"
        prompt += f"Stance: {'PRO (supporting)' if stance == Stance.PRO else 'CON (opposing)'}\n\n"
        
        prompt += "DRAFT ARGUMENT TO VERIFY:\n\n"
        prompt += f"{argument}\n\n"
        
        # Include debate context if it's not the first round
        if history:
            opponent_stance = Stance.CON if stance == Stance.PRO else Stance.PRO
            prompt += f"\nNote: This is round {len(history) + 1} of the debate. "
            prompt += f"The {opponent_stance.value} side has previously argued:\n\n"
            
            last_turn = history[-1]
            opponent_argument = last_turn.con_argument if stance == Stance.PRO else last_turn.pro_argument
            prompt += f"{opponent_argument[:300]}...\n\n"
        
        prompt += "Please verify this argument for logical soundness, factual accuracy, and persuasive strength.\n"
        prompt += "Then, provide an improved version that addresses any weaknesses while maintaining the original intent.\n"
        
        return prompt 