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
- Web interface for tracking agent status and viewing results

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
├── templates/            # Web interface templates
│   └── index.html        # Main web interface page
├── crew.py               # Agent and task orchestration
├── main.py               # CLI entry point
├── web_app.py            # Web interface application
├── run_web_interface.bat # Windows batch file to start web interface
├── run_web_interface.sh  # Unix/Linux shell script to start web interface
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running locally with the `deepseek-r1:7b` model
  - Install Ollama from: https://ollama.ai/download
  - Pull the model: `ollama pull deepseek-r1:7b`

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

### Command Line Interface

Run the market research tool via the command line:

```
python main.py --market "Electric Vehicles in India"
```

Examples of markets you can research:
- "Electric Vehicles in India"
- "Sustainable Fashion in Europe"
- "Cloud Gaming Services in North America"

### Web Interface

To use the web interface:

1. On Windows:
   ```
   run_web_interface.bat
   ```

2. On Unix/Linux/macOS:
   ```
   chmod +x run_web_interface.sh
   ./run_web_interface.sh
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

4. Enter the market you want to research and click "Start Research"

The web interface will show you:
- Current status of each agent
- Logs of the research process
- Final research results when complete

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
