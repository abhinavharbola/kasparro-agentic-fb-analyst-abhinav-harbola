# Kasparro Agentic FB Analyst

## Overview
An autonomous multi-agent system that diagnoses Facebook Ads performance.
Implements Planner, Insight, and Evaluator agents with a self-correcting loop.

## Architecture
[Planner] -> [Data Agent] -> [Insight Agent] -> [Evaluator] -> [Report]
                                      ^___________| (Retry loop if low confidence)

## Quick Start
1. Install dependencies:
   `pip install -r requirements.txt`
2. Run the analysis:
   `python run.py "Analyze why ROAS dropped last week"`

## Validation Strategy
The `EvaluatorAgent` performs strict quantitative checks on all LLM-generated insights using `pandas` aggregations before including them in the final report.
