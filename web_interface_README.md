# Market Research Crew - Web Interface

A user-friendly web interface for the Market Research Crew multi-agent system.

## Overview

This web interface provides a simple way to:
- Trigger market research for any topic
- Monitor the progress of each agent in real-time
- View detailed logs of the research process
- Access the final report in a readable format

## Features

- **Real-time Status Updates**: See what each agent is doing as they work
- **Live Logging**: View detailed logs of the entire research process
- **Agent Status Dashboard**: Monitor which agents are active, completed, or idle
- **Markdown Report Viewing**: View the final report in a nicely formatted way

## Getting Started

### Prerequisites

- Python 3.8 or higher
- All dependencies listed in `requirements.txt`
- Ollama or other compatible LLM service configured

### Installation

1. Make sure all requirements are installed:
   ```
   pip install -r requirements.txt
   ```

2. Make sure you have the LLM backend configured. By default, this uses Ollama with Phi-3-mini.

### Running the Web Interface

Start the web interface by running:

```
python app.py
```

This will start the server on http://localhost:5000

### Using the Interface

1. Open your browser and navigate to http://localhost:5000
2. Enter a market to research in the input field (e.g., "Electric Vehicles in India")
3. Click "Start Research" to begin the process
4. Monitor the progress in real-time:
   - The "Agent Status" panel shows which agents are active
   - The "Agent Logs" tab displays detailed logs of the process
5. When the research is complete, the "Results" tab will automatically show the final report

## How It Works

The web interface uses:
- Flask for the web server
- Socket.IO for real-time communication
- Bootstrap for the UI components
- CrewAI for the multi-agent orchestration

Each agent's progress is tracked through callbacks and sent to the frontend in real-time.

## Customization

You can customize the research agents and tasks by modifying the YAML configuration files in the `config` directory:
- `agents.yaml`: Define agent roles, goals, and tools
- `tasks.yaml`: Define research tasks and dependencies

## Troubleshooting

If you encounter issues:

1. Ensure Ollama is running and the model (phi3:mini) is available
2. Check that all dependencies are correctly installed
3. Look for errors in the console output or browser developer tools
4. Verify your network can connect to localhost:5000

## License

This project is open source and available under the MIT License. 