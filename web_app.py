"""
Market Research Crew - Web Interface
"""
import os
import threading
import queue
import json
import sys
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Set environment variables before importing any other libraries
os.environ.setdefault("OLLAMA_API_BASE", "http://localhost:11434")
if "OPENAI_API_BASE_URL" in os.environ:
    del os.environ["OPENAI_API_BASE_URL"]
if "OPENAI_API_KEY" in os.environ:
    del os.environ["OPENAI_API_KEY"]
os.environ['LITELLM_LOG'] = 'DEBUG'

try:
    from crew import SimplifiedCrew
except ImportError as e:
    print(f"Error importing SimplifiedCrew: {e}")
    print("Please check your installation and dependencies.")
    sys.exit(1)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Global variables to track research status and results
research_status = {
    "trend_analyst": "idle",
    "competitor_researcher": "idle",
    "data_synthesizer": "idle",
    "report_generator": "idle"
}
research_results = []
agent_logs = []
current_market = ""
research_in_progress = False
result_queue = queue.Queue()

@app.route('/')
def index():
    """Main page of the Market Research Crew web interface."""
    return render_template('index.html', 
                           research_status=research_status,
                           research_results=research_results,
                           agent_logs=agent_logs,
                           research_in_progress=research_in_progress,
                           current_market=current_market)

@app.route('/api/status')
def get_status():
    """API endpoint to get the current research status."""
    return jsonify({
        "status": research_status,
        "in_progress": research_in_progress,
        "current_market": current_market,
        "agent_logs": agent_logs[-10:] if agent_logs else []  # Return only the last 10 logs
    })

@app.route('/api/results')
def get_results():
    """API endpoint to get the current research results."""
    return jsonify({
        "results": research_results
    })

@app.route('/api/research', methods=['POST'])
def start_research():
    """API endpoint to start a market research process."""
    global research_in_progress, current_market, research_status, research_results, agent_logs
    
    if research_in_progress:
        return jsonify({"error": "Research already in progress"}), 400
    
    data = request.json
    market = data.get('market', '')
    
    if not market:
        return jsonify({"error": "No market specified"}), 400
    
    # Reset status and results
    research_status = {
        "trend_analyst": "idle",
        "competitor_researcher": "idle",
        "data_synthesizer": "idle",
        "report_generator": "idle"
    }
    research_results = []
    agent_logs = []
    current_market = market
    research_in_progress = True
    
    # Start research in a background thread
    thread = threading.Thread(target=run_research, args=(market,))
    thread.daemon = True
    thread.start()
    
    return jsonify({"message": f"Started research for {market}"})

def status_callback(agent_id, status, message=None):
    """Callback function to update agent status."""
    global research_status, agent_logs
    
    if agent_id in research_status:
        research_status[agent_id] = status
    
    if message:
        log_entry = f"{agent_id}: {message}"
        agent_logs.append(log_entry)
        print(f"[WebApp] {log_entry}")

def run_research(market):
    """Run the market research process in the background."""
    global research_in_progress, research_results
    
    try:
        # Initialize the crew with status callback
        market_research_crew = SimplifiedCrew(config_dir="config", status_callback=status_callback)
        
        # Set up the research input
        research_input = {"market": market}
        
        # Update status callback is handled by the crew now
        agent_logs.append(f"Starting research on {market}")
        
        # Run the crew
        result = market_research_crew.run(run_input=research_input)
        
        # Store the result
        research_results = [result]
        
        # Update final status
        agent_logs.append(f"Research completed for {market}")
    
    except Exception as e:
        # Handle any exceptions
        error_message = f"Error during research: {str(e)}"
        agent_logs.append(error_message)
        print(f"[WebApp] {error_message}")
        
        # Update status to "error" for all agents
        for agent_id in research_status:
            research_status[agent_id] = "error"
    
    finally:
        # Mark research as no longer in progress
        research_in_progress = False

if __name__ == "__main__":
    # Ensure the templates directory exists
    if not os.path.exists("templates"):
        os.makedirs("templates")
    
    # Ensure the static directory exists
    if not os.path.exists("static"):
        os.makedirs("static")
    
    print("Starting Market Research Crew Web Interface on http://127.0.0.1:5000")
    
    try:
        # Start the Flask app
        app.run(debug=False, host="127.0.0.1", port=5000)
    except Exception as e:
        print(f"Error starting Flask application: {e}")
        sys.exit(1) 