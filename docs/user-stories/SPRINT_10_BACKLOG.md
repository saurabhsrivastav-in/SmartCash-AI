# 🌍 Sprint 10 Backlog: Zero-Touch Global Scaling

**Sprint Goal:** Expand the engine to support multi-entity hierarchies and implement high-volume data partitioning for global enterprise deployment.

---

## 🏗️ Story 10.1: Multi-Entity "Intercompany" Hierarchy
**User Persona:** As a Global Controller, I want to toggle between different regional subsidiaries (e.g., North America, EMEA, APAC) so that I can monitor localized liquidity within a consolidated dashboard.

### 📝 Description
Implement a "Company Code" filter layer. The system must partition invoices and bank feeds by `Entity_ID`, allowing for both a "Consolidated View" and a "Subsidiary-Specific View."

### ✅ Acceptance Criteria
- [ ] **Hierarchical Filtering:** The sidebar includes a multi-select for "Global Entities."
- [ ] **Data Isolation:** Ensure Analysts in the "APAC" group cannot view "EMEA" transactions unless granted "Global" permissions.
- [ ] **Consolidation:** The **Liquidity Bridge** correctly aggregates multi-currency balances into a single "Reporting Currency" (e.g., USD) using real-time mock FX rates.



---

## 🏗️ Story 10.2: High-Volume Data Partitioning (50k+ Records)
**User Persona:** As a Treasury IT Lead, I want the system to remain responsive when processing 50,000+ open invoices so that the UI doesn't lag during peak month-end closing.

### 📝 Description
Refactor the data ingestion layer to move from flat CSV loading to a partitioned "Data Lake" approach. Implement "Lazy Loading" for the Analyst Workbench so only active transactions are rendered.

### ✅ Acceptance Criteria
- [ ] **Performance:** Dashboard load time remains < 3 seconds with a 50k row dataset.
- [ ] **Memory Optimization:** Utilize `pandas` dtypes optimization to reduce the RAM footprint of the `st.session_state` cache.
- [ ] **Pagination:** The Analyst Workbench implements a "Load More" or paginated view for unmatched items.

---

## 🏗️ Story 10.3: Regional Tax & VAT Handling logic
**User Persona:** As a Tax Manager, I want the system to identify VAT/GST components in bank credits so that we don't accidentally over-match net invoice amounts.

### 📝 Description
Develop logic to identify and separate tax components in countries with complex VAT requirements (e.g., India, UK, Germany). The engine must recognize "Gross" vs. "Net" payment scenarios.

### ✅ Acceptance Criteria
- [ ] **Tax Gate:** Match engine identifies if `Bank_Amount` includes `VAT_Percentage` calculated on the `Invoice_Net_Amount`.
- [ ] **Status:** Flagged as `STATUS_TAX_ADJUSTMENT` in the Audit Ledger.
- [ ] **Validation:** GenAI Agent is updated to request "Tax Withholding Certificates" for payments where the variance matches regional tax rates.



---

## 🏗️ Story 10.4: Global Setting & Localization
**User Persona:** As a Regional AR Lead, I want to see dates, currencies, and numbers formatted in my local standard so that I can avoid interpretation errors.

### 📝 Description
Implement a "Localization Profile" in the user settings. This affects date formats (DD/MM vs MM/DD), number separators, and primary local currency displays.

### ✅ Acceptance Criteria
- [ ] **Formatting:** UI dynamically updates based on `Locale` (e.g., switching from $1,234.56 to 1.234,56 €).
- [ ] **Timezone Sync:** The `Match_Timestamp` in the Audit Ledger displays in both UTC and the User’s local timezone.
- [ ] **Language Support:** Basic framework for multi-language labels (i18n) in the sidebar and navigation.

---

## 🚀 Technical Sub-tasks for Developers
1. **Infrastructure:** Optimize `st.cache_data` TTL (Time-To-Live) for large datasets.
2. **Logic Expansion:** Update `backend/engine.py` to support multi-entity data frames.
3. **UI Polish:** Implement "Quick Filters" for top-performing subsidiaries.
4. **Mock Data:** Update `mock_data_maker.py` to generate data across 10 distinct `Company_Codes` and regional tax variances.
