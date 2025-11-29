import pandas as pd
from src.agents.evaluator_agent import EvaluatorAgent

def test_evaluator_logic():
    # Create fake data where CTR drops
    data = {'ctr': [0.05, 0.04, 0.01], 'date': ['1', '2', '3']}
    df = pd.DataFrame(data)
    
    agent = EvaluatorAgent()
    result = agent.validate("CTR dropped significantly", df)
    
    assert result['is_validated'] == True
    assert result['confidence_score'] > 0.9