"""
Printer utilities for the debate agent team
"""
from typing import List, Dict, Any
import json
from debate_duel.shared.schemas import Turn

class DebateAgentPrinter:
    """Utility for printing debug information during the debate generation process"""
    
    def __init__(self):
        self.section_width = 80
    
    def print_section(self, section_name: str):
        """Print a section header"""
        print("\n" + "=" * self.section_width)
        print(f"{section_name}".center(self.section_width))
        print("=" * self.section_width + "\n")
    
    def print_topic(self, topic: str):
        """Print the debate topic"""
        print(f"🎯 TOPIC: {topic}\n")
    
    def print_history(self, history: List[Turn]):
        """Print debate history"""
        print("📜 DEBATE HISTORY:")
        for i, turn in enumerate(history):
            print(f"\nRound {i+1}:")
            print(f"PRO: {turn.pro_argument[:150]}...")
            print(f"CON: {turn.con_argument[:150]}...")
            if turn.judge_decision:
                print(f"JUDGE: {turn.judge_decision.winner} | {turn.judge_decision.justification[:100]}...")
        print("\n")
    
    def print_plan(self, plan: Dict[str, Any]):
        """Print the debate plan"""
        print("🗺️ PLAN:")
        for key, value in plan.items():
            if isinstance(value, list):
                print(f"\n{key.upper()}:")
                for i, item in enumerate(value):
                    print(f"  {i+1}. {item}")
            else:
                print(f"\n{key.upper()}: {value}")
        print("\n")
    
    def print_research(self, research: Dict[str, str]):
        """Print research results"""
        print("🔍 RESEARCH RESULTS:")
        for point, info in research.items():
            print(f"\n[{point}]")
            print(f"{info[:200]}...")
        print("\n")
    
    def print_strategy(self, strategy: Dict[str, Any]):
        """Print debate strategy"""
        print("⚔️ STRATEGY:")
        for key, value in strategy.items():
            if isinstance(value, list):
                print(f"\n{key.upper()}:")
                for i, item in enumerate(value):
                    print(f"  {i+1}. {item}")
            else:
                print(f"\n{key.upper()}: {value}")
        print("\n")
    
    def print_draft(self, argument: str):
        """Print draft argument"""
        print("📝 DRAFT ARGUMENT:")
        print(f"\n{argument[:500]}...\n")
    
    def print_verified(self, argument: str):
        """Print verified argument"""
        print("✅ VERIFIED ARGUMENT:")
        print(f"\n{argument[:500]}...\n")
        print("-" * self.section_width)
        print("ARGUMENT GENERATION COMPLETE".center(self.section_width))
        print("-" * self.section_width + "\n") 