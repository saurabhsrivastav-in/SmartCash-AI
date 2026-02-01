import pytest
from backend.treasury import TreasuryManager

@pytest.fixture
def treasury():
    return TreasuryManager()

def test_fx_conversion(treasury):
    """Verifies currency conversion logic (e.g., EUR to USD)."""
    # Assuming treasury has a convert method: amount, from_curr, to_curr
    converted = treasury.convert_currency(100, "EUR", "USD")
    # Using a standard mock rate of 1.1 for test stability
    assert converted == 110.0

def test_liquidity_buffer_alert(treasury):
    """Checks if low liquidity triggers a warning."""
    # amount, threshold
    status = treasury.check_liquidity_buffer(5000, 10000)
    assert status == "CRITICAL: Below Threshold"

def test_sweep_logic(treasury):
    """Verifies that excess cash is identified for investment sweeps."""
    sweep_amount = treasury.calculate_investment_sweep(150000, target_balance=100000)
    assert sweep_amount == 50000
