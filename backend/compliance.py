import pandas as pd
class ComplianceGuard:
    def __init__(self):
        self.logs = []
    def log_transaction(self, tx_id, action, user="AI"):
        self.logs.append({"Timestamp": "2026-01-29", "TX": tx_id, "Action": action, "User": user})
    def get_logs(self):
        return pd.DataFrame(self.logs)
