class EvaluatorAgent:
    def validate(self, hypothesis, df):
        """Quantitatively verifies if the LLM's insight is true."""
        confidence = 0.0
        is_validated = False
        
        # Logic: If hypothesis mentions CTR, check if CTR is actually trending down
        if "ctr" in hypothesis.lower():
            start_ctr = df.iloc[0]['ctr']
            end_ctr = df.iloc[-1]['ctr']
            
            if end_ctr < start_ctr:
                confidence = 0.95
                is_validated = True
                verification = "Verified: CTR dropped from start to end of period."
            else:
                confidence = 0.2
                verification = "Failed: Data shows CTR increased or stayed flat."
        else:
            verification = "No quantifiable metric found in hypothesis."

        return {
            "is_validated": is_validated,
            "confidence_score": confidence,
            "reasoning": verification
        }