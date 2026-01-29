from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fuzzywuzzy import process

app = FastAPI(title="SmartCash AI Matching Engine")

# --- Mock ERP Data ---
OPEN_INVOICES = [
    {"id": "INV-1001", "customer": "Walmart", "amount": 5000.00},
    {"id": "INV-1002", "customer": "Amazon", "amount": 1250.50},
    {"id": "INV-1003", "customer": "Target", "amount": 300.00},
]

class Payment(BaseModel):
    payer_name: str
    amount: float
    remittance_ref: Optional[str] = None

@app.post("/match")
async def match_payment(payment: Payment):
    """
    The Core Logic: Matches incoming payment to open invoices.
    A PM would call this the 'Auto-Match Workflow'.
    """
    results = []
    
    # 1. Exact Match Check (Reference & Amount)
    for inv in OPEN_INVOICES:
        if payment.remittance_ref == inv["id"] and payment.amount == inv["amount"]:
            return {"status": "MATCHED", "invoice_id": inv["id"], "confidence": 1.0, "reason": "Exact Match"}

    # 2. Fuzzy Matching (Payer Name + Amount)
    invoice_names = [inv["customer"] for inv in OPEN_INVOICES]
    best_match_name, score = process.extractOne(payment.payer_name, invoice_names)
    
    matched_inv = next((inv for inv in OPEN_INVOICES if inv["customer"] == best_match_name), None)
    
    if score > 80 and matched_inv["amount"] == payment.amount:
        return {
            "status": "SUGGESTED",
            "invoice_id": matched_inv["id"],
            "confidence": score / 100,
            "reason": "Customer name fuzzy match with exact amount"
        }

    # 3. Exception Handling (Short Payment)
    if matched_inv and payment.amount < matched_inv["amount"]:
        return {
            "status": "EXCEPTION",
            "invoice_id": matched_inv["id"],
            "reason": "Short Payment Detected",
            "deduction_amount": matched_inv["amount"] - payment.amount
        }

    raise HTTPException(status_code=404, detail="No match found. Sent to Analyst Workbench.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
