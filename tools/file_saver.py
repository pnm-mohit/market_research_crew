"""
File Saver Tool for CrewAI agents to save reports to disk.
"""
import os
import logging
from datetime import datetime
from typing import Optional
from langchain.tools import Tool
from crewai.tools.base_tool import Tool as CrewTool

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Define the output directory
OUTPUT_DIR = "reports"

# Create the output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def save_file(content: str, filename: Optional[str] = None, market: Optional[str] = None) -> str:
    """
    Save content to a file.
    
    Args:
        content: The text content to save
        filename: Optional filename to use (default: auto-generated based on date and market)
        market: Optional market name to include in the auto-generated filename
        
    Returns:
        A string indicating success or failure
    """
    try:
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            market_str = f"_{market.replace(' ', '_')}" if market else ""
            filename = f"market_research{market_str}_{timestamp}.md"
        
        # Ensure the filename has an extension
        if not filename.endswith(('.txt', '.md', '.pdf', '.docx')):
            filename += '.md'
        
        # Create the full file path
        file_path = os.path.join(OUTPUT_DIR, filename)
        
        logger.info(f"Saving file to {file_path}")
        
        # Write the content to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Successfully saved report to {file_path}")
        return f"Successfully saved report to {file_path}"
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        return f"Error saving file: {str(e)}"

# Create the FileSaverTool using LangChain's Tool class
_langchain_file_saver_tool = Tool(
    name="File Saver",
    description="Save content to a file on disk.",
    func=save_file
)

# Adapt the langchain Tool to a CrewAI Tool (subclass of BaseTool)
FileSaverTool = CrewTool.from_langchain(_langchain_file_saver_tool)

# Provide a logger accessor if needed
def get_logger():
    return logger

# Define a global function to log FileSaverTool actions
def log_file_saver(message, level="info"):
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "debug":
        logger.debug(message)
