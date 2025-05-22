"""
CrewAI Tool Adapter - Converts langchain Tools to CrewAI compatible tools
"""
import logging
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class CrewAIToolAdapter:
    """
    Adapter class that makes langchain Tools compatible with CrewAI.
    
    This class wraps a langchain Tool and provides the necessary interface
    that CrewAI expects for its tools.
    """
    
    def __init__(self, tool):
        """
        Initialize the adapter with a langchain Tool.
        
        Args:
            tool: A langchain Tool instance
        """
        self.tool = tool
        self.name = tool.name
        self.description = tool.description
        
        # Copy over any public attributes from the original tool
        for attr_name in dir(tool):
            if not attr_name.startswith('_') and attr_name not in ['name', 'description', 'run', 'func']:
                if hasattr(tool, attr_name):
                    setattr(self, attr_name, getattr(tool, attr_name))
    
    def run(self, *args, **kwargs) -> str:
        """Run the tool with the provided arguments."""
        logger.info(f"Running tool: {self.name} with args: {args}, kwargs: {kwargs}")
        try:
            result = self.tool.run(*args, **kwargs)
            logger.info(f"Tool {self.name} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Error running tool {self.name}: {str(e)}")
            raise

def adapt_langchain_tool(tool):
    """
    Convert a langchain Tool to a CrewAI compatible tool.
    
    Args:
        tool: A langchain Tool instance
        
    Returns:
        A CrewAIToolAdapter instance that wraps the tool
    """
    return CrewAIToolAdapter(tool) 