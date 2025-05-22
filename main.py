"""
Market Research Crew - CLI Entry Point
"""
import os
import argparse
from dotenv import load_dotenv
from crew import SimplifiedCrew

# Load environment variables
load_dotenv()

# --- Setup Logging (Optional but Recommended) ---
# import logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Main Execution ---
def main():
    """
    Main function to initialize and run the Simplified Crew for market research.
    """
    print("Starting the Market Research Crew...")

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run market research on a specified market')
    parser.add_argument('--market', type=str, help='Market to research')
    args = parser.parse_args()

    # Initialize the crew
    try:
        market_research_crew = SimplifiedCrew(config_dir="config")
    except FileNotFoundError as e:
        print(f"Error initializing crew: Config file not found. {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred during crew initialization: {e}")
        return

    # Define the market to research - either from args or default
    market_to_research = args.market if args.market else "Electric Vehicles in India"
    
    # This will be used to format the task descriptions in tasks.yaml
    research_input = {"market": market_to_research}

    print(f"Running market research for: {research_input['market']}")

    # Run the crew
    try:
        result = market_research_crew.run(run_input=research_input)
        print("\n--- Crew Execution Finished ---")
        print("Final Result from the Market Research Crew:")
        print(result)

        # The report generation is now handled by the report_generator agent using the file_saver_tool
        # No need to manually save the output here as it's done by the agent

    except Exception as e:
        print(f"An error occurred during the crew execution: {e}")
        print("Please check your Ollama server, configurations, and model names.")
        # You might want to print the full traceback for debugging
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
