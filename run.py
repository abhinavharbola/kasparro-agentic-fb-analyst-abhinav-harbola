import argparse
import yaml
import os
from dotenv import load_dotenv
from src.orchestrator import AgentOrchestrator
from src.utils import setup_logging

# Load API Key from .env
load_dotenv()

def main():
    # 1. Load Config
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    # 2. Setup Logging
    logger = setup_logging(config)
    
    # 3. Parse Args
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Analysis query", default="Analyze ROAS drop")
    args = parser.parse_args()
    
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY not found in .env file.")
        return

    logger.info(f"Starting Analysis: {args.query}")
    print(f"Agent System Running on {config['system']['model']}...")
    
    # 4. Orchestrate
    orchestrator = AgentOrchestrator(config)
    orchestrator.run(args.query)
    
    print("\nAnalysis Complete. Check /reports folder.")

if __name__ == "__main__":
    main()