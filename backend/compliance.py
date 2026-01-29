import pandas as pd
from datetime import datetime, timedelta
import random

class ComplianceGuard:
    def __init__(self):
        # The 'vault' is a list of dictionary events
        self.vault = []
        self._generate_mock_audit_trail()

    def log_transaction(self, invoice_id, action_type, user="AI_AGENT_STP"):
        """Logs a new event to the vault in real-time"""
        new_entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Event_ID": f"LOG-{random.randint(1000, 9999)}",
            "Invoice_Ref": invoice_id,
            "Action": action_type,
            "Operator": user,
            "Status": "Verified",
            "Hash_ID": hex(random.getrandbits(64)) # Simulating blockchain/immutable hashing
        }
        self.vault.insert(0, new_entry) # Add to top

    def _generate_mock_audit_trail(self):
        """Populates the vault with historical data for the demo"""
        actions = ["AUTO_MATCH_STP", "MANUAL_OVERRIDE", "STRESS_TEST_ADJ", "TREASURY_SWEEP"]
        users = ["AI_AGENT_STP", "TREASURY_MGR_01", "SYSTEM_ROOT", "AUDIT_BOT"]
        
        for i in range(15):
            past_time = datetime.now() - timedelta(hours=i*2, minutes=random.randint(1, 59))
            self.vault.append({
                "Timestamp": past_time.strftime("%Y-%m-%d %H:%M:%S"),
                "Event_ID": f"LOG-{random.randint(1000, 9999)}",
                "Invoice_Ref": f"INV-10{random.randint(10, 99)}",
                "Action": random.choice(actions),
                "Operator": random.choice(users),
                "Status": "Verified",
                "Hash_ID": hex(random.getrandbits(64))
            })

    def get_logs(self):
        """Returns the vault as a clean DataFrame for Streamlit"""
        return pd.DataFrame(self.vault)
