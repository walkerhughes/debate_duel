"""
Team-based swarm agent that implements the same interface as the original SwarmAgent
but uses a team of specialized agents to generate debate arguments.
"""
from typing import List

from debate_duel.shared.schemas import ArgumentRequest, Turn, Stance
from debate_duel.agents.team_debater.manager import DebateAgentManager


class TeamSwarmAgent:
    """
    A team-based swarm agent that uses specialized agents to collaboratively
    generate strategic debate arguments.
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the team swarm agent.
        
        Args:
            verbose: Whether to print detailed output during argument generation
        """
        self.debate_team = DebateAgentManager(verbose=verbose)
    
    def generate_argument(self, request: ArgumentRequest) -> str:
        """
        Generate an argument for the given topic based on the debate history
        using a team of specialized agents.
        
        Args:
            request: The request containing topic, stance, and debate history
            
        Returns:
            Generated argument as a string
        """
        return self.debate_team.generate_argument(request)


# For backwards compatibility, also create a class with the same name as the original
class SwarmAgent(TeamSwarmAgent):
    """Alias for TeamSwarmAgent for backwards compatibility"""
    pass 