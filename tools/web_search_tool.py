"""
Web Search Tool for CrewAI agents using DuckDuckGo.
"""
import requests
import logging
from typing import List, Dict, Any, Optional
from pydantic import Field
from langchain.tools import Tool
from duckduckgo_search import DDGS
from crewai.tools.base_tool import Tool as CrewTool

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def web_search(query: str, max_results: int = 5) -> str:
    """
    Execute a web search using DuckDuckGo.
    
    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 5)
        
    Returns:
        A string containing the search results
    """
    try:
        logger.info(f"Executing web search for: {query}")
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            logger.warning(f"No results found for query: {query}")
            return "No results found for the query."
        
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_result = f"{i}. {result['title']}\n"
            formatted_result += f"   URL: {result['href']}\n"
            formatted_result += f"   Summary: {result['body']}\n"
            formatted_results.append(formatted_result)
        
        logger.info(f"Found {len(results)} results for query: {query}")
        return "\n".join(formatted_results)
    except Exception as e:
        logger.error(f"Error performing web search: {str(e)}")
        return f"Error performing web search: {str(e)}"


# Create the WebSearchTool using LangChain's Tool class
_langchain_web_search_tool = Tool(
    name="Web Search",
    description="Search the web for information using DuckDuckGo.",
    func=web_search
)

# Adapt the langchain Tool to a CrewAI Tool (subclass of BaseTool)
WebSearchTool = CrewTool.from_langchain(_langchain_web_search_tool)

# Provide a logger accessor if needed
def get_logger():
    return logger

# Define a global function to log WebSearchTool actions
def log_web_search(message, level="info"):
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "debug":
        logger.debug(message)
