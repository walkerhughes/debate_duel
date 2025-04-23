# Agent Debate Duel

An environment for hosting strategic, team-based debates, where agents generate arguments across multiple turns. Agent teams use a deep-research inspired workflow to plan an approach to craft their argument, anticipate the opposing team's counter arguments, and refine their strategy across multi-turn debates. An LLM-as-a-Judge evaluates each round and selects winners, enabling the creation of datasets for supervised fine-tuning/RLHF via Outcome Reward Modeling or Policy Reward Modeling.

Note: When creating synthetic data generated this way, take precaution to ensure that the model learns strategic argumentation patterns rather than domain-specific content — since winning arguments may be tied to hot-button topics, fine-tuning on this data without careful curation could inadvertently encode topical biases rather than generalizable reasoning skills.


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

This collaborative approach allows for more strategic, well-researched, and persuasive arguments compared to a single-agent approach, as the team of agents prepares an argument conditioned on anticipated counter arguments and their potential weaknesses.

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

### Running a Debate from the Command Line

You can run a test argument with the below code, replacing your topic in the quotations:

```
python -m debate_duel.agents.team_debater.client --topic "Should open-source AI be regulated?" --stance pro --verbose
```

Output will appear beginning with the research process undertaken by the team of agents:

```
Generating PRO argument for topic: Should open-source AI models be regulated?

================================================================================
                  STARTING ARGUMENT GENERATION FOR PRO STANCE                   
================================================================================

🎯 TOPIC: Should open-source AI models be regulated?

🗺️ PLAN:

OVERALL_APPROACH: Advocate for the regulation of open-source AI models to ensure ethical standards, safety, and accountability in their development and deployment.

POINTS:
  1. Regulation is necessary to prevent misuse of open-source AI models, which can lead to harmful consequences such as misinformation, privacy violations, and autonomous weaponization.
  2. Establishing ethical guidelines will promote responsible innovation, ensuring that AI technologies benefit society while minimizing risks associated with their deployment.
  3. Regulation will enhance public trust in AI technologies by ensuring transparency and accountability in their development and use, addressing concerns about bias and discrimination.
  4. A regulatory framework can foster collaboration between developers, policymakers, and stakeholders, creating a balanced approach to innovation and safety in AI development.

OPPONENT_WEAKNESSES:
  1. The opponents may argue that regulation stifles innovation; however, historical examples show that well-defined regulations can actually promote responsible innovation and public confidence.
  2. They may claim that open-source models are inherently safe due to community oversight, but this overlooks the potential for malicious actors to exploit vulnerabilities without proper guidelines.
  3. The assertion that market forces alone can ensure safety is flawed, as it neglects the potential for economic incentives to prioritize profit over ethical considerations.

ANTICIPATED_COUNTERARGUMENTS:
  1. Opponents may argue that regulation will hinder the rapid development of AI technologies, suggesting that innovation thrives in an unregulated environment.
  2. They might claim that the existing community oversight of open-source projects provides sufficient checks and balances without the need for formal regulation.
  3. Another counterargument could be that regulation could create barriers for smaller developers and startups, leading to a monopolization of the AI field by larger corporations.
  .
  .
  .

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
