import pytest
from app.models import Loan

def test_apply_for_loan(client, auth_headers, test_customer, db_session):
    """Test loan application."""
    loan_data = {
        "loan_type": "personal",
        "amount": 50000,
        "tenure_months": 24,
        "interest_rate": 12.5
    }
    response = client.post("/customers/loans", json=loan_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["loan_type"] == "personal"
    assert data["amount"] == 50000
    assert data["status"] == "pending"
    assert data["emi"] is None  # Not calculated yet

def test_get_customer_loans(client, auth_headers, test_customer, db_session):
    """Test getting customer's loan history."""
    # Create a loan first
    loan = Loan(
        customer_id=test_customer.id,
        loan_type="home",
        amount=200000,
        tenure_months=120,
        interest_rate=8.5,
        status="approved",
        emi=2500.50
    )
    db_session.add(loan)
    db_session.commit()

    response = client.get("/customers/loans", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["loan_type"] == "home"
    assert data[0]["status"] == "approved"

def test_get_pending_loans_admin(client, admin_auth_headers, db_session, test_customer):
    """Test admin viewing pending loans."""
    # Create a pending loan
    loan = Loan(
        customer_id=test_customer.id,
        loan_type="car",
        amount=30000,
        tenure_months=36,
        interest_rate=10.0,
        status="pending"
    )
    db_session.add(loan)
    db_session.commit()

    response = client.get("/admins/loans", headers=admin_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["loan_type"] == "car"
    assert data[0]["status"] == "pending"
    assert data[0]["emi"] is not None  # Should be calculated for admin view

def test_approve_loan(client, admin_auth_headers, db_session, test_customer):
    """Test admin approving a loan."""
    # Create a pending loan
    loan = Loan(
        customer_id=test_customer.id,
        loan_type="education",
        amount=40000,
        tenure_months=48,
        interest_rate=9.0,
        status="pending"
    )
    db_session.add(loan)
    db_session.commit()
    loan_id = loan.id

    # Approve the loan
    response = client.put(f"/admins/loans/{loan_id}", json={"status": "approved"}, headers=admin_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "approved"
    assert data["emi"] is not None  # EMI should be calculated and saved

def test_reject_loan(client, admin_auth_headers, db_session, test_customer):
    """Test admin rejecting a loan."""
    # Create a pending loan
    loan = Loan(
        customer_id=test_customer.id,
        loan_type="business",
        amount=100000,
        tenure_months=60,
        interest_rate=15.0,
        status="pending"
    )
    db_session.add(loan)
    db_session.commit()
    loan_id = loan.id

    # Reject the loan
    response = client.put(f"/admins/loans/{loan_id}", json={"status": "rejected"}, headers=admin_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "rejected"
    assert data["emi"] is None  # No EMI for rejected loans

def test_approve_non_pending_loan(client, admin_auth_headers, db_session, test_customer):
    """Test approving a loan that's not pending."""
    # Create an approved loan
    loan = Loan(
        customer_id=test_customer.id,
        loan_type="personal",
        amount=25000,
        tenure_months=12,
        interest_rate=11.0,
        status="approved",
        emi=2200.00
    )
    db_session.add(loan)
    db_session.commit()
    loan_id = loan.id

    # Try to approve again
    response = client.put(f"/admins/loans/{loan_id}", json={"status": "approved"}, headers=admin_auth_headers)
    assert response.status_code == 400
    assert "not pending" in response.json()["detail"]

def test_update_nonexistent_loan(client, admin_auth_headers):
    """Test updating a loan that doesn't exist."""
    response = client.put("/admins/loans/999", json={"status": "approved"}, headers=admin_auth_headers)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_customer_access_admin_endpoint(client, auth_headers):
    """Test customer trying to access admin endpoint."""
    response = client.get("/admins/loans", headers=auth_headers)
    assert response.status_code == 403

def test_unauthorized_access(client):
    """Test accessing protected endpoints without authentication."""
    response = client.post("/customers/loans", json={"loan_type": "test", "amount": 1000, "tenure_months": 12, "interest_rate": 5})
    assert response.status_code == 401

    response = client.get("/customers/me")
    assert response.status_code == 401

    response = client.get("/admins/loans")
    assert response.status_code == 401