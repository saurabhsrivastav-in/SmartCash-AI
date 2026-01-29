# SmartCash AI: Next-Gen Cash Application Automation

**SmartCash AI** is a high-performance automated cash application engine designed to eliminate manual reconciliation in the Order-to-Cash (O2C) cycle. 

Unlike legacy solutions like HighRadius, SmartCash AI prioritizes **Explainable AI matching** and **Real-time ERP synchronization**, giving AR analysts 100% visibility into why payments were matched or flagged.

## 📊 Product Vision (PM Perspective)
The goal of this project is to achieve a **95% Straight-Through Processing (STP) rate** by automating the three biggest bottlenecks in AR:
1. **Remittance Ingestion:** Automated extraction from unstructured PDFs/Emails.
2. **Intelligent Matching:** Multi-factor logic (Invoice #, Amount, Customer Name, and Historical patterns).
3. **Exception Management:** A "Human-in-the-loop" UI for rapid resolution of short-payments and unidentified deductions.

## 🚀 Key Features vs. Competitors
| Feature | HighRadius / Legacy | SmartCash AI |
| :--- | :--- | :--- |
| **Matching Logic** | Black-box AI | **Explainable AI** (Confidence scores & reason codes) |
| **Integration** | Heavy ERP footprint | **API-First** (Headless or UI-driven) |
| **User Experience** | Complex, menu-heavy | **Action-oriented Dashboard** |
| **Deductions** | Manual coding | **Auto-categorization** of trade/non-trade claims |

## 🛠️ Technical Stack
- **Backend:** Python (FastAPI) for high-concurrency processing.
- **AI/ML:** FuzzyWuzzy (string matching) & Scikit-learn for historical pattern recognition.
- **Frontend:** React + Tailwind CSS for a sleek Analyst Workbench.
- **Database:** PostgreSQL (simulating ERP tables).

## 🏃 Quick Start (Local Demo)
1. `pip install -r requirements.txt`
2. `python main.py`
3. Open `localhost:8000/docs` to see the Automated Posting API.
