import json
import os
from src.agents.planner_agent import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator_agent import EvaluatorAgent
from src.agents.creative_agent import CreativeAgent
from src.utils import setup_logging

class AgentOrchestrator:
    def __init__(self, config):
        self.config = config
        self.logger = setup_logging(config)

    def run(self, query):
        self.logger.info(f"Received Query: {query}")

        # 1. Planner Agent (New!)
        self.logger.info("🤖 Planner Agent: Decomposing task...")
        planner = PlannerAgent(self.config)
        plan = planner.plan(query)
        self.logger.info(f"Plan created: {plan.get('steps', [])}")
        
        # 2. Data Agent
        self.logger.info("📊 Data Agent: Loading & Summarizing data...")
        data_agent = DataAgent(self.config)
        df, summary = data_agent.run()
        
        # 3. Insight Agent (New!)
        self.logger.info("💡 Insight Agent: Generating Hypotheses...")
        insight_agent = InsightAgent(self.config)
        insight_data = insight_agent.analyze(summary)
        
        # 4. Evaluator Agent
        self.logger.info("⚖️ Evaluator Agent: Validating Hypotheses...")
        evaluator = EvaluatorAgent()
        validation = evaluator.validate(insight_data['hypothesis'], df)
        
        results = {
            "query": query,
            "plan": plan,
            "insight": insight_data,
            "validation": validation,
            "creatives": []
        }

        # 5. Creative Agent (Conditional)
        if validation['is_validated']:
            self.logger.info("🎨 Hypothesis Validated! Generating Creatives...")
            creative_agent = CreativeAgent(self.config)
            creatives = creative_agent.generate(summary['low_performing_ads'])
            results['creatives'] = json.loads(creatives)
        else:
            self.logger.warning("Hypothesis not validated. Skipping creative generation.")

        # 6. Save Reports
        self.save_reports(results)
        return results

    def save_reports(self, results):
        os.makedirs(self.config['paths']['reports'], exist_ok=True)
        # Save JSON
        with open(f"{self.config['paths']['reports']}/insights.json", "w") as f:
            json.dump(results, f, indent=2)
        
        # Generate Markdown Report
        report_path = f"{self.config['paths']['reports']}/report.md"
        with open(report_path, "w") as f:
            f.write(f"# Analysis Report: {results['query']}\n\n")
            f.write(f"## 1. Insight\n{results['insight']['hypothesis']}\n\n")
            f.write(f"## 2. Validation\n**Verified:** {results['validation']['is_validated']}\n")
            f.write(f"**Confidence:** {results['validation']['confidence_score']}\n\n")
            
            if results['creatives']:
                f.write("## 3. Recommended Creatives\n")
                if 'recommendations' in results['creatives']:
                    for rec in results['creatives']['recommendations']:
                        f.write(f"* {rec}\n")