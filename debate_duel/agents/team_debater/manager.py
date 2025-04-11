"""
Manager for the team of debate agents - coordinates the workflow between different agents
"""
from typing import List, Dict, Any
from debate_duel.shared.schemas import ArgumentRequest, Turn, Stance
from debate_duel.settings.constants import OPENAI_CLIENT, OPENAI_MODEL

from debate_duel.agents.team_debater.agents.planner import PlannerAgent
from debate_duel.agents.team_debater.agents.researcher import ResearcherAgent
from debate_duel.agents.team_debater.agents.strategist import StrategistAgent
from debate_duel.agents.team_debater.agents.writer import WriterAgent 
from debate_duel.agents.team_debater.agents.verifier import VerifierAgent
from debate_duel.agents.team_debater.printer import DebateAgentPrinter


class DebateAgentManager:
    """Manager that coordinates the workflow between different debate agent specialists"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.printer = DebateAgentPrinter() if verbose else None
        
        # Initialize the specialist agents
        self.planner = PlannerAgent()
        self.researcher = ResearcherAgent()
        self.strategist = StrategistAgent()
        self.writer = WriterAgent()
        self.verifier = VerifierAgent()
    
    def generate_argument(self, request: ArgumentRequest) -> str:
        """
        Generate a strategic argument by coordinating multiple specialized agents
        
        Args:
            request: The request containing topic, stance, and debate history
            
        Returns:
            Generated argument as a string
        """
        topic = request.topic
        stance = request.stance
        history = request.history
        
        if self.verbose:
            self.printer.print_section(f"STARTING ARGUMENT GENERATION FOR {stance.value.upper()} STANCE")
            self.printer.print_topic(topic)
            if history:
                self.printer.print_history(history)
        
        # Step 1: Planning - Identify key areas to address
        plan = self.planner.create_plan(topic, stance, history)
        if self.verbose:
            self.printer.print_plan(plan)
        
        # Step 2: Research - Gather information on key points
        research_results = self.researcher.research_points(topic, plan["points"])
        if self.verbose:
            self.printer.print_research(research_results)
        
        # Step 3: Strategy - Determine effective arguments and structure
        strategy = self.strategist.develop_strategy(
            topic, 
            stance, 
            history, 
            plan, 
            research_results
        )
        if self.verbose:
            self.printer.print_strategy(strategy)
        
        # Step 4: Writing - Craft the final argument
        argument = self.writer.write_argument(
            topic,
            stance,
            history,
            plan,
            research_results,
            strategy
        )
        if self.verbose:
            self.printer.print_draft(argument)
        
        # Step 5: Verification - Check for soundness and identify weaknesses
        verified_argument = self.verifier.verify_argument(
            topic,
            stance,
            history,
            argument
        )
        if self.verbose:
            self.printer.print_verified(verified_argument)
        
        return verified_argument 