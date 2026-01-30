# 🧠 Sprint 2 Backlog: Intelligence & Fuzzy Match Engine

**Sprint Goal:** Implement the Level 2 "Fuzzy Match" gate to identify payers with >90% accuracy despite "dirty" bank data and mismatched naming conventions.

---

## 🏗️ Story 2.1: Advanced Fuzzy Logic Integration
**User Persona:** As an AR Analyst, I want the system to identify "Tesla Inc" even if the bank feed says "Tesla Ltd" so that I don't have to manually search for the customer.

### 📝 Description
Integrate the `thefuzz` library into the `SmartMatchingEngine`. This gate should calculate the Levenshtein distance between the `Bank_Payer_Name` and the `ERP_Customer_Name`.

### ✅ Acceptance Criteria
- [ ] **Heuristic Gate:** Logic triggered if Level 1 (Exact Match) fails.
- [ ] **Similarity Scoring:** System calculates a ratio (0-100) using `token_set_ratio`.
- [ ] **Threshold:** Returns a match suggestion only if the score is > 85.
- [ ] **Multi-Currency FX Handling:** Allows for a +/- 1% variance in amount to account for bank fees/FX fluctuations.



---

## 🏗️ Story 2.2: The Analyst Workbench (UI/UX)
**User Persona:** As an AR Analyst, I want a dedicated interface to review "Suggested Matches" so I can maintain control over high-value postings.

### 📝 Description
Develop the **Analyst Workbench** view in Streamlit. This interface allows the user to select a bank transaction and see the top AI-suggested invoice matches.

### ✅ Acceptance Criteria
- [ ] **Focus Dropdown:** Selectable list of unmatched bank transactions.
- [ ] **Suggestion Display:** Shows the Top 3 matches with their corresponding confidence scores.
- [ ] **Manual Override:** Button to "Confirm Match" which then triggers the SOC2 Vault logging.

---

## 🏗️ Story 2.3: Predictive DSO Drift Modeling
**User Persona:** As a Treasurer, I want to see a forecast of our DSO trends so I can predict liquidity shortfalls before they happen.

### 📝 Description
Utilize `scipy.stats` to perform linear regression on historical payment dates. This should visualize the "Drift" caused by the Macro Stress slider.

### ✅ Acceptance Criteria
- [ ] **Trendline:** Display a Plotly line chart showing historical vs. forecasted DSO.
- [ ] **Stress Interaction:** The forecast window (shaded area) must shift dynamically based on the "Collection Latency" slider.
- [ ] **Accuracy Metric:** Display the $R^2$ value of the trend to show statistical confidence.

---

## 🏗️ Story 2.4: Risk Radar Sunburst (Level 2)
**User Persona:** As a Risk Manager, I want to see where our cash is concentrated so I can identify exposure to high-risk customers.

### 📝 Description
Enhance the **Risk & Governance** view with a multi-level Sunburst chart. This chart must drill down from Currency -> Customer -> ESG Score.



### ✅ Acceptance Criteria
- [ ] **Hierarchy:** Correct rendering of the path: `['Currency', 'Customer', 'ESG_Score']`.
- [ ] **Color Mapping:** 'AA' and 'A' scores appear Green; 'C' scores appear Red.
- [ ] **Scaling:** The size of each segment must be proportional to the `Invoice_Amount`.

---

## 🚀 Technical Sub-tasks for Developers
1. **Library Update:** Add `thefuzz` and `python-Levenshtein` to `requirements.txt`.
2. **Backend Logic:** Refine `backend/engine.py` to include `process.extractOne` logic.
3. **Data Science:** Implement `get_dso_forecast` function in `main.py` using `scipy.stats.linregress`.
4. **Mock Data:** Update `mock_data_maker.py` to add "Ltd", "Group", or "LLC" suffixes to 50% of bank names to test fuzzy accuracy.
