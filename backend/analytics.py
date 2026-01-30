import pandas as pd
import numpy as np

class TreasuryAnalytics:
    """
    Advanced Quantitative Engine for SmartCash AI.
    Handles liquidity forecasting, ESG risk weighting, and stress-test simulations.
    """
    
    def __init__(self):
        self.opening_cash_balance = 125000000  # $125M starting point

    def calculate_esg_risk_score(self, df_inv):
        """
        Calculates a weighted risk score based on ESG tiers (Sprint 5).
        Returns a distribution used for the Risk Radar.
        """
        # Mapping ESG ratings to numeric risk multipliers
        risk_map = {'AA': 1.0, 'A': 1.1, 'B': 1.5, 'C': 2.5}
        
        df = df_inv.copy()
        df['Risk_Weight'] = df['ESG_Score'].map(risk_map)
        df['Weighted_Exposure'] = df['Amount'] * df['Risk_Weight']
        
        return df

    def run_liquidity_simulation(self, df_inv, stress_days):
        """
        Simulates cash arrival based on 'Collection Latency' slider (Sprint 8).
        Calculates the 'Haircut' or the amount of cash delayed due to risk factors.
        """
        # Total expected collections
        total_ar = df_inv['Amount'].sum()
        
        # Calculate daily velocity (simplified)
        daily_velocity = total_ar / 30 
        
        # The stress test: more latency = higher "Locked Cash"
        # We assume a 0.5% liquidity decay per day of delay
        haircut_multiplier = (stress_days * 0.005)
        stressed_haircut = total_ar * haircut_multiplier
        
        net_collections = total_ar - stressed_haircut
        
        return {
            "Opening_Balance": self.opening_cash_balance,
            "Expected_AR": total_ar,
            "Stressed_Haircut": stressed_haircut,
            "Net_Position": self.opening_cash_balance + net_collections
        }

    def get_dso_trends(self, df_inv):
        """
        Calculates Days Sales Outstanding (DSO) drift (Sprint 6).
        """
        # Simulated behavioral data for the demo
        avg_dso = 42.5  # Standard industry average
        drift = np.random.uniform(-5, 12) # Simulate monthly variance
        
        return round(avg_dso + drift, 2)

    def get_waterfall_data(self, df_inv, stress_days):
        """
        Formats data specifically for the Plotly Waterfall component.
        """
        sim = self.run_liquidity_simulation(df_inv, stress_days)
        
        # Conversion to Millions for readability
        data = {
            "x": ["Opening Cash", "Expected AR", "Stress Haircut", "Net Position"],
            "y": [
                sim["Opening_Balance"] / 1e6,
                sim["Expected_AR"] / 1e6,
                -sim["Stressed_Haircut"] / 1e6,
                0 # Plotly calculates the total automatically if measure is set
            ],
            "measure": ["relative", "relative", "relative", "total"]
        }
        return data
