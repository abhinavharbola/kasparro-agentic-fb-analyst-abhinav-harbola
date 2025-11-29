import pandas as pd

class DataAgent:
    def __init__(self, config):
        self.filepath = config['paths']['data']

    def run(self):
        df = pd.read_csv(self.filepath)
        # Summarize data for the LLM
        summary = {
            "total_spend": float(df['spend'].sum()),
            "avg_roas": float(df['roas'].mean()),
            "trend_ctr": df.groupby('date')['ctr'].mean().to_dict(),
            "low_performing_ads": df[df['roas'] < 1.5]['creative_message'].unique().tolist()
        }
        return df, summary