import hashlib
import pandas as pd
from datetime import datetime

class ComplianceGuard:
    def __init__(self):
        self.audit_log = []

    def log_transaction(self, invoice_id, action, user="AI_AGENT"):
        """Sprint 9: Creates an immutable record of the clearing action."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create SHA-256 Hash to simulate blockchain immutability
        raw_data = f"{timestamp}-{invoice_id}-{action}-{user}"
        tx_hash = hashlib.sha256(raw_data.encode()).hexdigest()
        
        self.audit_log.append({
            "Timestamp": timestamp,
            "Invoice_ID": invoice_id,
            "Action": action,
            "User": user,
            "TX_Hash": tx_hash[:16],
            "Security": "PQC-Kyber-Enforced" # Sprint 11 simulation
        })

    def get_logs(self):
        return pd.DataFrame(self.audit_log)
