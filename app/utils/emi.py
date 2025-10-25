def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
    """
    Calculate EMI using the formula: EMI = (P*r*(1+r)^n)/((1+r)^n-1)
    Where:
    P = principal amount
    r = monthly interest rate (annual_rate / 100 / 12)
    n = tenure in months
    """
    monthly_rate = annual_rate / 100 / 12
    if monthly_rate == 0 or tenure_months == 0:
        return principal / tenure_months if tenure_months > 0 else 0
    emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)
    return round(emi, 2)