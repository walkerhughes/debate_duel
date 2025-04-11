"""
Client script for testing the team debater system directly
"""
import argparse
from typing import List, Optional

from debate_duel.shared.schemas import ArgumentRequest, Stance, Turn, JudgeResponse, Winner
from debate_duel.agents.team_debater.manager import DebateAgentManager


def create_sample_history() -> List[Turn]:
    """Create a sample debate history for testing"""
    return [
        Turn(
            pro_argument="Universal healthcare is a fundamental right that should be guaranteed to all citizens. Countries with universal healthcare systems have better health outcomes, lower costs, and more equitable access to care. The moral imperative to ensure everyone can access necessary medical treatment outweighs concerns about implementation challenges.",
            con_argument="While healthcare access is important, universal healthcare systems are inefficient, reduce innovation, and lead to rationing of care. Free market solutions with targeted subsidies for those in need would better balance access and quality while preserving patient choice and provider autonomy.",
            judge_decision=JudgeResponse(
                winner=Winner.PRO,
                justification="The PRO side made a stronger case by emphasizing both moral and practical benefits of universal healthcare systems with specific references to outcomes in other countries."
            )
        )
    ]


def main():
    parser = argparse.ArgumentParser(description="Test the team debater system")
    parser.add_argument("--topic", type=str, default="Social media has a net positive impact on society",
                        help="Debate topic")
    parser.add_argument("--stance", type=str, choices=["pro", "con"], default="pro",
                        help="Stance to argue (pro or con)")
    parser.add_argument("--use-history", action="store_true",
                        help="Use sample debate history")
    parser.add_argument("--verbose", action="store_true",
                        help="Print verbose output")
    
    args = parser.parse_args()
    
    # Convert stance string to enum
    stance = Stance.PRO if args.stance.lower() == "pro" else Stance.CON
    
    # Create debate history if requested
    history = create_sample_history() if args.use_history else []
    
    # Create argument request
    request = ArgumentRequest(
        topic=args.topic,
        stance=stance,
        history=history
    )
    
    # Initialize the team debater manager
    team_debater = DebateAgentManager(verbose=args.verbose)
    
    # Generate the argument
    print(f"\nGenerating {stance.value.upper()} argument for topic: {args.topic}")
    if not args.verbose:
        print("Processing... (use --verbose for detailed output)")
    
    argument = team_debater.generate_argument(request)
    
    if not args.verbose:
        print("\n" + "=" * 80)
        print(f"FINAL {stance.value.upper()} ARGUMENT".center(80))
        print("=" * 80 + "\n")
        print(argument)
        print("\n" + "=" * 80)


if __name__ == "__main__":
    main() 