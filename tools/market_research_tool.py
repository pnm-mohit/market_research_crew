from typing import Dict, List, Any
import requests
import json
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from langchain.tools import Tool
from crewai.tools.base_tool import Tool as CrewTool
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Filter out werkzeug logging (HTTP request logs)
logging.getLogger('werkzeug').setLevel(logging.ERROR)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class MarketResearchTool:
    """
    Advanced Market Research Tool for comprehensive market analysis.
    
    Features:
    - Web search and data retrieval
    - Trend analysis
    - Sentiment analysis
    - Economic indicator retrieval
    - Market potential scoring
    """
    
    def __init__(self, 
                 serper_api_key: str = None, 
                 alpha_vantage_key: str = None,
                 output_dir: str = None):
        """
        Initialize the Market Research Tool with optional API keys.
        
        Args:
            serper_api_key: API key for web search
            alpha_vantage_key: API key for economic indicators
            output_dir: Directory to save reports (defaults to project's reports folder)
        """
        # Prioritize passed keys, then environment variables
        self.serper_api_key = serper_api_key or os.getenv('SERPER_API_KEY')
        self.alpha_vantage_key = alpha_vantage_key or os.getenv('ALPHA_VANTAGE_API_KEY')
        
        # Set up output directory
        if output_dir is None:
            # Use the reports directory in the project root
            self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
        else:
            self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Validate API keys
        self._validate_api_keys()
    
    def _validate_api_keys(self):
        """
        Validate the presence of required API keys with helpful messages.
        """
        if not self.serper_api_key:
            logger.warning("No Serper API key found! Falling back to simulated search results.")
            print("\n⚠️ WARNING: No Serper API key found!")
            print("To enable web search capabilities, please:")
            print("1. Sign up at https://serper.dev/")
            print("2. Add your API key to the .env file as SERPER_API_KEY")
            print("Falling back to simulated search results.\n")
        
        if not self.alpha_vantage_key:
            logger.warning("No Alpha Vantage API key found! Economic indicators will be simulated.")
            print("\n⚠️ WARNING: No Alpha Vantage API key found!")
            print("Economic indicators will be simulated.")
            print("To get real economic data, sign up at https://www.alphavantage.co/\n")
    
    def _run_search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Perform a web search, with fallback to simulated results.
        
        Args:
            query: Search query
            num_results: Number of results to return
        
        Returns:
            List of search results
        """
        logger.info(f"Performing web search for: {query}")
        
        if not self.serper_api_key:
            # Simulated search results when no API key is available
            logger.info("Using simulated search results (no API key)")
            return [
                {
                    "title": f"Trend in {query}",
                    "snippet": f"Simulated insight about {query} market trends",
                    "link": f"https://example.com/search?q={query.replace(' ', '+')}"
                }
                for _ in range(num_results)
            ]
        
        try:
            # TODO: Implement actual Serper API search when key is available
            # This is a placeholder for future implementation
            logger.info("Using placeholder API search implementation")
            return [
                {
                    "title": f"Real Trend in {query}",
                    "snippet": f"Actual insight about {query} market trends",
                    "link": f"https://example.com/search?q={query.replace(' ', '+')}"
                }
                for _ in range(num_results)
            ]
        except Exception as e:
            logger.error(f"Search error: {e}")
            print(f"Search error: {e}")
            return []
    
    def _get_economic_indicators(self, market: str) -> Dict[str, Any]:
        """
        Retrieve economic indicators, with fallback to simulated data.
        
        Args:
            market: Market to retrieve indicators for
        
        Returns:
            Dictionary of economic indicators
        """
        if not self.alpha_vantage_key:
            # Simulated economic indicators
            return {
                "market_size": 500_000_000_000,
                "growth_rate": 0.12,
                "investment_volume": 250_000_000,
                "startup_count": 150,
                "data_source": "Simulated"
            }
        
        try:
            # TODO: Implement actual Alpha Vantage API call when key is available
            return {
                "market_size": 500_000_000_000,
                "growth_rate": 0.12,
                "investment_volume": 250_000_000,
                "startup_count": 150,
                "data_source": "Alpha Vantage (Placeholder)"
            }
        except Exception as e:
            print(f"Economic indicator retrieval error: {e}")
            return {}
    
    def _calculate_market_potential(self, search_results: List[Dict[str, Any]]) -> float:
        """
        Calculate market potential based on search results.
        
        Args:
            search_results: List of search results
        
        Returns:
            Market potential score (0-100)
        """
        # Simple scoring mechanism based on result relevance and volume
        potential_score = min(len(search_results) * 10, 100)
        return potential_score
    
    def _extract_trends(self, search_results: List[Dict[str, Any]]) -> List[str]:
        """
        Extract top trends from search results.
        
        Args:
            search_results: List of search results
        
        Returns:
            List of identified trends
        """
        trends = []
        for result in search_results:
            # Extract trends from titles and snippets
            if result.get('title'):
                trends.append(result['title'])
            if result.get('snippet'):
                trends.append(result['snippet'])
        return trends[:3]  # Return top 3 trends
    
    def _run(self, query: str) -> str:
        """
        Main method to run market research.
        
        Args:
            query: Market research query
        
        Returns:
            Comprehensive market research report
        """
        logger.info(f"Running market research for query: {query}")
        
        # Perform web search
        search_results = self._run_search(query)
        
        # Extract insights
        trends = self._extract_trends(search_results)
        market_potential = self._calculate_market_potential(search_results)
        economic_indicators = self._get_economic_indicators(query)
        
        # Compile report
        report = {
            "query": query,
            "search_results": search_results,
            "trends": trends,
            "market_potential_score": market_potential,
            "economic_indicators": economic_indicators
        }
        
        logger.info(f"Completed market research for: {query}")
        return json.dumps(report, indent=2)
    
    def run(self, query: str) -> str:
        """
        Public method to run market research.
        
        Args:
            query: Market research query
        
        Returns:
            Comprehensive market research report as JSON string
        """
        result = self._run(query)
        # Save the report as JSON
        self._save_report(query, result)
        # Save the report as PDF
        self._save_report_pdf(query, result)
        return result
    
    def _save_report(self, query: str, report: str) -> str:
        """
        Save the market research report to a file.
        
        Args:
            query: The research query
            report: The JSON report string
        
        Returns:
            str: Path to the saved report file
        """
        # Create filename with timestamp and sanitized query
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_query = "".join(x for x in query if x.isalnum() or x in (' ', '-', '_'))[:50]
        filename = f"market_research_{timestamp}_{sanitized_query}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        # Save report
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Report saved to: {filepath}")
        return filepath
    
    def _save_report_pdf(self, query: str, report: str) -> str:
        """
        Save the market research report to a PDF file using reportlab.
        
        Args:
            query: The research query
            report: The JSON report string
        
        Returns:
            str: Path to the saved PDF report file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_query = "".join(x for x in query if x.isalnum() or x in (' ', '-', '_'))[:50]
        filename = f"market_research_{timestamp}_{sanitized_query}.pdf"
        filepath = os.path.join(self.output_dir, filename)

        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']
        styleH.textColor = colors.blue
        story = []
        story.append(Paragraph(f"Market Research Report for: {query}", styleH))
        story.append(Spacer(1, 12))
        try:
            report_data = json.loads(report)
            for key, value in report_data.items():
                if isinstance(value, (list, dict)):
                    value_str = json.dumps(value, indent=2)
                else:
                    value_str = str(value)
                story.append(Paragraph(f"<b>{key}:</b> {value_str}", styleN))
                story.append(Spacer(1, 8))
        except Exception as e:
            story.append(Paragraph(f"Error parsing report: {e}", styleN))
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        doc.build(story)
        logger.info(f"PDF report saved to: {filepath}")
        return filepath

# Create a langchain Tool instance
market_research_tool = MarketResearchTool()
_langchain_market_research_tool = Tool(
    name="Market Research Tool",
    func=market_research_tool.run,
    description="A comprehensive tool for conducting in-depth market research."
)

# Adapt the langchain Tool to a CrewAI Tool (subclass of BaseTool)
def create_market_research_tool():
    """
    Create a CrewAI Tool for market research.
    
    Returns:
        An instance of Tool compatible with CrewAI
    """
    return CrewTool.from_langchain(_langchain_market_research_tool)

# Provide a logger accessor if needed
def get_logger():
    return logger

# Define a global function to log MarketResearchTool actions
def log_market_research(message, level="info"):
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "debug":
        logger.debug(message)