import pytest
import pandas as pd
from backend.analytics import SmartAnalytics

@pytest.fixture
def analytics():
    return SmartAnalytics()

@pytest.fixture
def mock_invoice_data():
    """Generates a dataset to test aging and collection metrics."""
    return pd.DataFrame({
        'Invoice_ID': ['INV-001', 'INV-002', 'INV-003', 'INV-004'],
        'Amount': [1000, 2000, 3000, 4000],
        'Status': ['Paid', 'Open', 'Open', 'Paid'],
        'Due_Date': [
            pd.Timestamp.now() - pd.Timedelta(days=10),
            pd.Timestamp.now() - pd.Timedelta(days=45),
            pd.Timestamp.now() + pd.Timedelta(days=10),
            pd.Timestamp.now() - pd.Timedelta(days=5)
        ]
    })

def test_collection_efficiency_ratio(analytics, mock_invoice_data):
    """Verifies that the CER is calculated correctly based on Paid vs Total."""
    # Paid (1000 + 4000) / Total (10000) = 50%
    cer = analytics.calculate_cer(mock_invoice_data)
    assert cer == 0.5

def test_aging_buckets(analytics, mock_invoice_data):
    """Checks if invoices are correctly categorized into 0-30, 31-60, 61+ days."""
    report = analytics.generate_aging_report(mock_invoice_data)
    
    # INV-002 is 45 days overdue, should be in the 31-60 bucket
    assert report['31-60_days'].sum() == 2000
    assert '61+_days' in report.columns

def test_cash_forecasting(analytics, mock_invoice_data):
    """Verifies that future cash flow projections only include 'Open' invoices."""
    forecast = analytics.get_cash_forecast(mock_invoice_data)
    # Only INV-003 is 'Open' and due in the future (3000)
    assert forecast['upcoming_collections'] == 3000
