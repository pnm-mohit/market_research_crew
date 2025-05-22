"""
Market Research Crew - Agent and Task Orchestration
"""
import os
import yaml
from typing import Dict, List, Any, Optional, Callable
from crewai import Agent, Task, Crew
from crewai.llm import LLM # Import CrewAI's LLM wrapper
from dotenv import load_dotenv
import litellm

# Import tools
from tools.web_search_tool import WebSearchTool
from tools.file_saver import FileSaverTool

# Load environment variables from .env file
load_dotenv()

# --- Environment Configuration for Ollama with LiteLLM --- 
# For LiteLLM's direct 'ollama/' provider (used by crewai.LLM):
# LiteLLM expects OLLAMA_API_BASE to be the base URL of your Ollama server.
os.environ.setdefault("OLLAMA_API_BASE", "http://localhost:11434")

# Remove OpenAI specific env vars as we are targeting direct Ollama provider via prefix
if "OPENAI_API_BASE_URL" in os.environ:
    del os.environ["OPENAI_API_BASE_URL"]
if "OPENAI_API_KEY" in os.environ:
    del os.environ["OPENAI_API_KEY"]

# Enable LiteLLM verbose logging for debugging
# As per logs, this might be deprecated, os.environ['LITELLM_LOG'] = 'DEBUG' is preferred
# litellm.set_verbose = True 
os.environ['LITELLM_LOG'] = 'DEBUG'
# --- End Environment Configuration ---

class SimplifiedCrew:
    """
    Orchestrates a simplified crew of agents (e.g., for story generation or market research).
    """
    
    def __init__(self, config_dir: str = "config", status_callback: Optional[Callable] = None):
        """
        Initialize the Crew.
        Args:
            config_dir: Directory containing configuration files (default: "config")
            status_callback: Optional callback function to update agent status
        """
        self.config_dir = config_dir
        self.agents_config = self._load_config("agents.yaml")
        self.tasks_config = self._load_config("tasks.yaml")
        
        # Initialize tools
        self.tools = {
            "web_search_tool": WebSearchTool,
            "file_saver_tool": FileSaverTool
        }
        
        # Create output directory if it doesn't exist (though not used in this simple example)
        if not os.path.exists("reports"):
            os.makedirs("reports")
        
        self.status_callback = status_callback
    
    def _load_config(self, filename: str) -> Dict[str, Any]:
        """
        Load a YAML configuration file.
        Args:
            filename: Name of the YAML file to load
        Returns: Dictionary containing the configuration
        """
        config_path = os.path.join(self.config_dir, filename)
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    
    def _create_llm(self, llm_config: Dict[str, Any]) -> Any:
        """
        Creates a crewai.LLM instance for Ollama.
        Model name from llm_config (e.g., "ollama/phi3:mini") should INCLUDE the prefix.
        """
        # Model name from agents.yaml (e.g., "ollama/phi3:mini")
        prefixed_model_name = llm_config.get("model_name", "ollama/phi3:mini") 
        
        print(f"[SimplifiedCrew] Creating crewai.LLM with model: {prefixed_model_name} and OLLAMA_API_BASE: {os.getenv('OLLAMA_API_BASE')}")
        
        # Use crewai.LLM wrapper
        # It will use LiteLLM in the background. LiteLLM will pick up OLLAMA_API_BASE.
        return LLM(
            model=prefixed_model_name,
            base_url=os.getenv('OLLAMA_API_BASE'), # Explicitly pass api_base for clarity
            temperature=llm_config.get("temperature", 0.7)
            # No need to pass api_key for Ollama if not required by local setup
        )
    
    def _create_agents(self) -> Dict[str, Agent]:
        """
        Create agents based on configuration. Assigns tools if specified in agent's config.
        Returns: Dictionary of agent name to agent instance
        """
        agents = {}
        if "agents" not in self.agents_config or not self.agents_config["agents"]:
            print("[SimplifiedCrew] No agents found in agents.yaml configuration.")
            return agents
            
        for agent_id, agent_config in self.agents_config["agents"].items():
            llm = self._create_llm(agent_config["llm_config"])
            
            agent_tools = []
            if "tools" in agent_config and agent_config["tools"]:
                for tool_name in agent_config["tools"]:
                    if tool_name in self.tools:
                        agent_tools.append(self.tools[tool_name])
                    else:
                        print(f"[SimplifiedCrew] Warning: Tool '{tool_name}' specified for agent '{agent_id}' not found in initialized tools.")
            
            agent = Agent(
                role=agent_config["role"],
                goal=agent_config["goal"],
                backstory=agent_config.get("backstory", ""),
                verbose=agent_config.get("verbose", True),
                allow_delegation=agent_config.get("allow_delegation", False),
                tools=agent_tools, # Pass the instantiated tools
                llm=llm
            )
            agents[agent_id] = agent
            print(f"[SimplifiedCrew] Created agent: {agent_id} with role: {agent_config['role']} and tools: {[t.name for t in agent_tools]}")
            
            # Update status through callback
            if self.status_callback:
                self.status_callback(agent_id, "idle", f"Agent {agent_id} initialized")
            
        return agents
    
    def _create_tasks(self, agents: Dict[str, Agent]) -> List[Task]:
        """
        Create tasks based on configuration. 
        The 'topic' parameter is available if task descriptions need it.
        """
        tasks = []
        task_map = {}
        if "tasks" not in self.tasks_config or not self.tasks_config["tasks"]:
            print("[SimplifiedCrew] No tasks found in tasks.yaml configuration.")
            return tasks

        for task_id, task_config in self.tasks_config["tasks"].items():
            if task_config["agent"] not in agents:
                print(f"[SimplifiedCrew] Agent '{task_config['agent']}' for task '{task_id}' not found. Skipping task.")
                continue
            
            agent_instance = agents[task_config["agent"]]
            
            # Fill placeholders in task description and expected_output
            # For this simple case, we assume a 'topic' might be in run_input later,
            # but tasks.yaml has {topic} so we need to handle it, even if just by replacing with a generic value for now.
            # A more robust solution would pass the actual run_input to this method.
            # For now, we'll make description dynamic in run()
            
            current_task_description = task_config["description"] # Will be formatted in run()
            current_expected_output = task_config["expected_output"] # Will be formatted in run()

            task = Task(
                description=current_task_description,
                expected_output=current_expected_output,
                agent=agent_instance,
                callbacks=[self._task_callback]  # Add callback
            )
            tasks.append(task)
            task_map[task_id] = task
            print(f"[SimplifiedCrew] Created task: {task_id} for agent: {task_config['agent']}")
        
        for task_id, task_config in self.tasks_config["tasks"].items():
            if task_id in task_map and "dependencies" in task_config and task_config["dependencies"]:
                context_tasks = [task_map[dep_id] for dep_id in task_config["dependencies"] if dep_id in task_map]
                if len(context_tasks) == len(task_config["dependencies"]):
                    task_map[task_id].context = context_tasks
                    print(f"[SimplifiedCrew] Set dependencies for task '{task_id}': {[dep.description[:30] + '...' for dep in context_tasks]}")
                else:
                    print(f"[SimplifiedCrew] Could not satisfy all dependencies for task '{task_id}'. Check task names in dependencies.")
        return tasks
    
    def _task_callback(self, event_type, agent, task=None, **kwargs):
        """Callback to track task progress and update agent status."""
        if not self.status_callback:
            return
        
        agent_id = None
        status = "idle"
        message = None
        
        # Get agent ID from task's agent (using role as fallback)
        if agent:
            for aid, a_config in self.agents_config["agents"].items():
                if a_config["role"] == agent.role:
                    agent_id = aid
                    break
        
        if not agent_id:
            return
            
        # Handle different event types
        if event_type == "task_started":
            status = "working"
            message = f"Starting task: {task.description[:50]}..."
        elif event_type == "task_completed":
            status = "completed"
            message = "Task completed"
        elif event_type == "task_failed":
            status = "error"
            message = f"Task failed: {kwargs.get('exception', 'Unknown error')}"
        elif event_type == "agent_started":
            status = "working"
            message = "Agent started"
        elif event_type == "agent_finished":
            status = "completed"
            message = "Agent finished"
            
        # Update status through callback
        self.status_callback(agent_id, status, message)
    
    def run(self, run_input: Dict[str, str]) -> str:
        """
        Run the crew for the specified input dictionary.
        Args:
            run_input: Dictionary containing inputs for the crew run (e.g., {"topic": "AI in healthcare"})
        Returns: The final result from the crew
        """
        print(f"[SimplifiedCrew] Starting crew run with input: {run_input}")
        
        # Create agents (tools are now handled within _create_agents)
        agents = self._create_agents()
        if not agents:
            return "Error: No agents were created. Check agent configuration."

        # Create tasks and format their descriptions/expected_outputs with run_input
        formatted_tasks = []
        task_map = {} # For dependency linking of newly formatted tasks

        if "tasks" not in self.tasks_config or not self.tasks_config["tasks"]:
            print("[SimplifiedCrew] No tasks found in tasks.yaml configuration.")
            return "Error: No tasks were created. Check task configuration."

        for task_id, task_config in self.tasks_config["tasks"].items():
            if task_config["agent"] not in agents:
                print(f"[SimplifiedCrew] Agent '{task_config['agent']}' for task '{task_id}' not found. Skipping task.")
                continue
            
            agent_instance = agents[task_config["agent"]]
            
            try:
                formatted_description = task_config["description"].format(**run_input)
                formatted_expected_output = task_config["expected_output"].format(**run_input)
            except KeyError as e:
                print(f"[SimplifiedCrew] Error: Missing key {e} in run_input for formatting task '{task_id}'. Using raw description/output.")
                formatted_description = task_config["description"]
                formatted_expected_output = task_config["expected_output"]

            task = Task(
                description=formatted_description,
                expected_output=formatted_expected_output,
                agent=agent_instance,
                callbacks=[self._task_callback]  # Add callback
            )
            formatted_tasks.append(task)
            task_map[task_id] = task # Store for dependency linking
            print(f"[SimplifiedCrew] Formatted task: {task_id} for agent: {task_config['agent']} with desc: {formatted_description[:50]}...")

        # Link dependencies for formatted tasks
        for task_id, task_config in self.tasks_config["tasks"].items():
            if task_id in task_map and "dependencies" in task_config and task_config["dependencies"]:
                current_task_object = task_map[task_id]
                context_tasks = []
                for dep_id in task_config["dependencies"]:
                    if dep_id in task_map:
                        context_tasks.append(task_map[dep_id])
                    else:
                        # This case should ideally not happen if all tasks are processed
                        print(f"[SimplifiedCrew] Dependency task '{dep_id}' for task '{task_id}' not found in task_map during formatting.")
                
                if len(context_tasks) == len(task_config["dependencies"]):
                    current_task_object.context = context_tasks
                    print(f"[SimplifiedCrew] Set dependencies for formatted task '{task_id}': {[dep.description[:30] + '...' for dep in context_tasks]}")

                else:
                    print(f"[SimplifiedCrew] Could not satisfy all dependencies for formatted task '{task_id}'.")


        if not formatted_tasks:
            return "Error: No tasks were created after formatting. Check task configuration or agent assignment."
        
        crew = Crew(
            agents=list(agents.values()),
            tasks=formatted_tasks, # Use the formatted tasks
            verbose=True, # Changed from 2 to True as Crew expects boolean
            process="sequential"
        )
        try:
            result = crew.kickoff()
            print(f"[SimplifiedCrew] Crew run completed. Result: {result}")
            return str(result)
        except Exception as e:
            print(f"[SimplifiedCrew] Error during crew kickoff: {e}")
            raise
