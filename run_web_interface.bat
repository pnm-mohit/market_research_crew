@echo off
echo Checking if Ollama is running...
curl -s http://localhost:11434/api/version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Ollama is not running. Please start it and try again.
    echo You can start it by running: ollama serve
    exit /b 1
)

echo Checking if deepseek-r1:7b model is available...
ollama list | findstr "deepseek-r1:7b" > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Model deepseek-r1:7b is not pulled. Would you like to pull it now? (y/n)
    set /p response=
    if /i "%response%"=="y" (
        echo Pulling deepseek-r1:7b model (this may take a while)...
        ollama pull deepseek-r1:7b
    ) else (
        echo Cannot continue without the model. Please modify config/agents.yaml to use a different model.
        exit /b 1
    )
)

echo Starting Market Research Crew Web Interface...
python web_app.py 