import pytest
from app.utils import calculate_emi

def test_calculate_emi_basic():
    """Test basic EMI calculation."""
    principal = 100000
    rate = 12  # 12%
    tenure = 12  # 12 months
    emi = calculate_emi(principal, rate, tenure)
    assert isinstance(emi, float)
    assert emi > 0
    # Expected EMI calculation
    expected = 8884.88  # Approximate
    assert abs(emi - expected) < 0.01

def test_calculate_emi_zero_rate():
    """Test EMI with zero interest rate."""
    principal = 50000
    rate = 0
    tenure = 10
    emi = calculate_emi(principal, rate, tenure)
    assert emi == 5000  # Simple division

def test_calculate_emi_zero_tenure():
    """Test EMI with zero tenure."""
    principal = 100000
    rate = 10
    tenure = 0
    emi = calculate_emi(principal, rate, tenure)
    assert emi == 0

def test_calculate_emi_high_rate():
    """Test EMI with high interest rate."""
    principal = 50000
    rate = 25
    tenure = 24
    emi = calculate_emi(principal, rate, tenure)
    assert emi > principal / tenure  # Should be higher than simple division

def test_calculate_emi_long_tenure():
    """Test EMI with long tenure."""
    principal = 100000
    rate = 8
    tenure = 240  # 20 years
    emi = calculate_emi(principal, rate, tenure)
    assert emi > 0
    assert emi < principal / tenure * 3  # Reasonable range for long tenure

def test_calculate_emi_precision():
    """Test EMI calculation precision."""
    principal = 100000
    rate = 12
    tenure = 12
    emi = calculate_emi(principal, rate, tenure)
    # Should be rounded to 2 decimal places
    assert emi == round(emi, 2)