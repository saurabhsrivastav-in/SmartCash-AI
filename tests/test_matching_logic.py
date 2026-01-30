import pytest
import pandas as pd
from backend.engine import SmartMatchingEngine

@pytest.fixture
def setup_engine():
    """Initializes the engine and mock data for testing."""
    engine = SmartMatchingEngine()
    mock_invoices = pd.DataFrame([
        {'Invoice_ID': 'INV-1001', 'Customer_Name': 'Tesla Inc', 'Amount': 50000, 'Currency': 'USD'},
        {'Invoice_ID': 'INV-1002', 'Customer_Name': 'Microsoft Corp', 'Amount': 75000, 'Currency': 'USD'},
        {'Invoice_ID': 'INV-1003', 'Customer_Name': 'SpaceX', 'Amount': 25000, 'Currency': 'EUR'}
    ])
    return engine, mock_invoices

def test_exact_match(setup_engine):
    """Scenario A: Verify 1:1 Exact Match (Reference & Amount)."""
    engine, df_inv = setup_engine
    # Simulating a perfect bank credit
    bank_txn = {'Bank_Ref': 'INV-1001', 'Amount': 50000, 'Currency': 'USD'}
    
    results = engine.run_match(bank_txn, df_inv)
    
    assert not results.empty
    assert results.iloc[0]['Invoice_ID'] == 'INV-1001'
    assert results.iloc[0]['Confidence_Score'] == 100

def test_fuzzy_name_match(setup_engine):
    """Scenario B: Verify Fuzzy Logic when the name is misspelled."""
    engine, df_inv = setup_engine
    # 'Tesla' misspelled as 'Tessla' and no Invoice ID provided
    bank_txn = {'Bank_Ref': 'Tessla Payment', 'Amount': 50000, 'Currency': 'USD'}
    
    results = engine.run_match(bank_txn, df_inv)
    
    assert not results.empty
    assert results.iloc[0]['Invoice_ID'] == 'INV-1001'
    assert results.iloc[0]['Confidence_Score'] >= 80

def test_short_pay_exception(setup_engine):
    """Scenario C: Verify handling of partial payments."""
    engine, df_inv = setup_engine
    # Correct ID, but the amount is short by 1000
    bank_txn = {'Bank_Ref': 'INV-1001', 'Amount': 49000, 'Currency': 'USD'}
    
    results = engine.run_match(bank_txn, df_inv)
    
    assert not results.empty
    # It should find the match but flag a variance
    assert results.iloc[0]['Invoice_ID'] == 'INV-1001'
    assert results.iloc[0]['Match_Type'] == 'Partial/Exception'

def test_no_match_found(setup_engine):
    """Scenario D: Verify system correctly fails when no data matches."""
    engine, df_inv = setup_engine
    bank_txn = {'Bank_Ref': 'Unknown Global Corp', 'Amount': 999999, 'Currency': 'JPY'}
    
    results = engine.run_match(bank_txn, df_inv)
    
    # Depending on your engine logic, this should return an empty DF or low score
    if not results.empty:
        assert results.iloc[0]['Confidence_Score'] < 50
