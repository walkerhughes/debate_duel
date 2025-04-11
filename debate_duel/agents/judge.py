from openai import OpenAI

from debate_duel.settings.constants import OPENAI_MODEL
from debate_duel.shared.schemas import JudgeRequest, JudgeResponse, Winner


class JudgeAgent:
    def __init__(self):
        self.client = OpenAI()
    
    def judge_debate(self, request: JudgeRequest) -> JudgeResponse:
        """
        Judge a debate round based on the pro and con arguments.
        
        Args:
            request: The request containing the topic and arguments
            
        Returns:
            A judgment with winner and justification
        """
        topic = request.topic
        pro_argument = request.pro_argument
        con_argument = request.con_argument
        
        # Construct the prompt
        prompt = self._build_prompt(topic, pro_argument, con_argument)
        
        # Call the OpenAI API
        response = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1024
        )
        
        content = response.choices[0].message.content
        
        # Parse the response
        winner, justification = self._parse_response(content)
        
        return JudgeResponse(
            winner=winner,
            justification=justification
        )
    
    def _get_system_prompt(self) -> str:
        """
        Get the system prompt for the judge.
        """
        return (
            "You are an impartial debate judge. Your goal is to fairly evaluate arguments from both sides of a debate "
            "and determine which side presented the stronger case. Consider logical reasoning, evidence, rhetorical "
            "effectiveness, and how well each side addressed the other's arguments. "
            "You must select a winner or declare a tie, and provide a clear justification for your decision."
        )
    
    def _build_prompt(self, topic: str, pro_argument: str, con_argument: str) -> str:
        """
        Build the prompt for the LLM.
        """
        prompt = f"Topic: {topic}\n\n"
        prompt += "Pro Argument:\n" + pro_argument + "\n\n"
        prompt += "Con Argument:\n" + con_argument + "\n\n"
        prompt += (
            "Please evaluate both arguments and determine which side made the stronger case.\n"
            "Your response must follow this format exactly:\n\n"
            "Winner: [pro|con|tie]\n"
            "Justification: [Your detailed justification for the decision]"
        )
        
        return prompt
    
    def _parse_response(self, content: str) -> tuple[Winner, str]:
        """
        Parse the LLM response to extract the winner and justification.
        """
        lines = content.strip().split("\n")
        
        winner_line = None
        justification_text = []
        justification_started = False
        
        for line in lines:
            if line.lower().startswith("winner:"):
                winner_line = line
            elif line.lower().startswith("justification:"):
                justification_started = True
                # Add the rest of this line excluding "Justification:"
                remainder = line.split(":", 1)[1].strip()
                if remainder:
                    justification_text.append(remainder)
            elif justification_started:
                justification_text.append(line)
        
        if not winner_line:
            return Winner.TIE, "No clear winner could be determined from the judge's response."
        
        winner_value = winner_line.split(":", 1)[1].strip().lower()
        if winner_value == "pro":
            winner = Winner.PRO
        elif winner_value == "con":
            winner = Winner.CON
        else:
            winner = Winner.TIE
        
        justification = " ".join(justification_text)
        if not justification:
            justification = "No justification provided."
        
        return winner, justification 