#!/usr/bin/env python
"""
Example client for the Debate Duel API.
"""
import asyncio
import json
import httpx
import argparse
from typing import Dict, Any


async def run_debate(topic: str, num_turns: int) -> Dict[str, Any]:
    """
    Run a debate using the Debate Duel API.
    
    Args:
        topic: The debate topic
        num_turns: Number of debate turns
        
    Returns:
        The full debate result
    """
    async with httpx.AsyncClient(timeout=300.0) as client:
        url = "http://localhost:8000/debate"
        payload = {
            "topic": topic,
            "num_turns": num_turns
        }
        
        response = await client.post(url, json=payload)
        response.raise_for_status()
        
        return response.json()


def display_debate(result: Dict[str, Any]) -> None:
    """
    Display the debate results in a readable format.
    
    Args:
        result: The debate result from the API
    """
    print("\n" + "=" * 80)
    print(f"DEBATE TOPIC: {result['topic']}")
    print("=" * 80)
    
    # Display ELO information
    print(f"\nInitial ELO - Pro: {result['initial_elo']['pro']}, Con: {result['initial_elo']['con']}")
    print(f"Final ELO   - Pro: {result['final_elo']['pro']}, Con: {result['final_elo']['con']}")
    print(f"Final Winner: {result['final_winner'].upper()}")
    
    # Display each turn
    for i, turn in enumerate(result['turns']):
        print(f"\n{'-' * 80}")
        print(f"ROUND {i + 1}")
        print(f"{'-' * 80}")
        
        print("\nPRO ARGUMENT:")
        print(turn['pro_argument'])
        
        print("\nCON ARGUMENT:")
        print(turn['con_argument'])
        
        print("\nJUDGE DECISION:")
        if turn.get('judge_decision'):
            print(f"Winner: {turn['judge_decision']['winner'].upper()}")
            print(f"Justification: {turn['judge_decision']['justification']}")
        else:
            print("No decision available")
    
    # Display ELO trajectory
    print("\nELO TRAJECTORY:")
    for i, elo in enumerate(result['elo_trajectory']):
        print(f"Round {i}: Pro: {elo['pro']}, Con: {elo['con']}")


async def main() -> None:
    """Main function to parse arguments and run the debate."""
    parser = argparse.ArgumentParser(description="Run a debate using the Debate Duel API")
    parser.add_argument("--topic", type=str, default="Artificial intelligence will benefit humanity in the long run",
                      help="The debate topic")
    parser.add_argument("--turns", type=int, default=2,
                      help="Number of debate turns")
    parser.add_argument("--output", type=str, 
                      help="Output file to save the JSON results (optional)")
    
    args = parser.parse_args()
    
    print(f"Running debate on topic: {args.topic}")
    print(f"Number of turns: {args.turns}")
    print("This may take a few minutes depending on the response time of the LLM...\n")
    
    result = await run_debate(args.topic, args.turns)
    
    # Save to file if specified
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nResults saved to {args.output}")
    
    # Display the results
    display_debate(result)


if __name__ == "__main__":
    asyncio.run(main()) 