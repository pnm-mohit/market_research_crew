#!/bin/bash

# Ensure Ollama is running
echo "Checking if Ollama is running..."
if ! curl -s http://localhost:11434/api/version > /dev/null; then
  echo "Ollama is not running. Please start it and try again."
  echo "You can start it by running: ollama serve"
  exit 1
fi

# Check if deepseek-r1:7b model is pulled
echo "Checking if deepseek-r1:7b model is available..."
if ! ollama list | grep -q "deepseek-r1:7b"; then
  echo "Model deepseek-r1:7b is not pulled. Would you like to pull it now? (y/n)"
  read response
  if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "Pulling deepseek-r1:7b model (this may take a while)..."
    ollama pull deepseek-r1:7b
  else
    echo "Cannot continue without the model. Please modify config/agents.yaml to use a different model."
    exit 1
  fi
fi

# Start the web interface
echo "Starting Market Research Crew Web Interface..."
python web_app.py 