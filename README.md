# Debate Duel

A system for conducting AI debates with strategic team-based argument generation.

## Overview

Debate Duel is a platform that facilitates debates between AI agents. It features:

- PRO and CON stance agents that generate strategic arguments
- A judge agent that evaluates the arguments and determines a winner
- An ELO-based rating system to track agent performance over time
- A team-based swarm approach for strategic argument generation

## Team-Based Approach

The new team-based approach uses multiple specialized agents working together to generate stronger, more strategic arguments:

1. **Planner Agent**: Analyzes the debate history and identifies key areas to address
2. **Researcher Agent**: Gathers information on key points for the debate argument
3. **Strategist Agent**: Determines effective arguments and their structure
4. **Writer Agent**: Crafts the final debate argument
5. **Verifier Agent**: Checks the argument for soundness and identifies weaknesses

This collaborative approach allows for more strategic, well-researched, and persuasive arguments compared to a single-agent approach.

## Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/debate-duel.git
   cd debate-duel
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set your OpenAI API key:
   ```
   export OPENAI_API_KEY=your_api_key_here
   ```

### Running a Debate

You can run a test debate with:

```
python -m debate_duel.agents.team_debater.client --topic "Your debate topic" --stance pro --verbose
```

## Project Structure

- `debate_duel/shared/`: Common schemas and utilities
- `debate_duel/settings/`: Configuration and constants
- `debate_duel/agents/`: AI agents for debate generation
  - `swarm.py`: Original single-agent implementation
  - `team_swarm.py`: New team-based implementation
  - `team_debater/`: Team of specialized agents
    - `agents/`: Individual specialized agents
    - `manager.py`: Coordinates the agent workflow
    - `printer.py`: Utilities for debug output
  - `judge/`: Debate judging agents

## License

This project is licensed under the MIT License - see the LICENSE file for details.
