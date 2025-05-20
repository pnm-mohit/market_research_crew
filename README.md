# Market Research Crew

A Python project using CrewAI and Ollama that performs automated market research using a multi-agent architecture. This system runs entirely locally, leveraging Ollama for local LLM inference.

## Overview

This project implements a multi-agent system for market research with four specialized agents:

1. **Trend Analyst**: Identifies top 3 current trends for a given market
2. **Competitor Researcher**: Identifies top 3 competitors and summarizes their strengths/weaknesses
3. **Data Synthesizer**: Combines findings into 3 strategic insights
4. **Report Generator**: Formats all outputs into a final saved report

## Features

- Fully offline operation using Ollama for local LLM inference
- Web search capabilities via DuckDuckGo
- Automatic report generation and saving
- Configurable agents and tasks via YAML files
- Simple CLI interface

## Project Structure

```
market_research_crew/
├── config/
│   ├── agents.yaml       # Agent configurations
│   └── tasks.yaml        # Task configurations
├── tools/
│   ├── __init__.py       # Package initialization
│   ├── web_search_tool.py # DuckDuckGo search tool
│   └── file_saver.py     # Tool for saving reports
├── crew.py               # Agent and task orchestration
├── main.py               # CLI entry point
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running locally with the `llama3` model
  - Install Ollama from: https://ollama.ai/download
  - Pull the Llama3 model: `ollama pull llama3`

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd market_research_crew
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Ensure Ollama is running:
   ```
   ollama serve
   ```

## Usage

Run the market research tool via the command line:

```
python main.py
```

You will be prompted to enter a market to research, for example:
- "Electric Vehicles in India"
- "Sustainable Fashion in Europe"
- "Cloud Gaming Services in North America"

Alternatively, you can specify the market directly:

```
python main.py --market "Electric Vehicles in India"
```

The system will:
1. Analyze current trends in the specified market
2. Research top competitors and their strengths/weaknesses
3. Synthesize the data into strategic insights
4. Generate a comprehensive report
5. Save the report to the `reports/` directory

## Customization

### Modifying Agents

Edit `config/agents.yaml` to:
- Change agent roles, goals, or backstories
- Adjust LLM parameters (temperature, max tokens)
- Modify tool access for agents

### Modifying Tasks

Edit `config/tasks.yaml` to:
- Change task descriptions or expected outputs
- Modify task dependencies
- Adjust task priorities or execution mode

## License

[MIT License](LICENSE)
