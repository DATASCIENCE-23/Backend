"""
Route sanity test for Finance Accounting Module
Run with: python check_routes.py
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def assert_ok(response, name):
    if response.status_code not in (200, 201):
        print(f"❌ {name} failed:", response.status_code, response.json())
        raise Exception(f"{name} failed")
    print(f" {name} passed")

# ---------------------------
# ACCOUNT
# ---------------------------
def test_account():
    r = client.post("/accounts", json={
        "account_name": "Cash",
        "account_type": "Asset"
    })
    assert_ok(r, "Create Account")
    account_id = r.json()["account_id"]

    r = client.get(f"/accounts/{account_id}")
    assert_ok(r, "Get Account")

    return account_id

# ---------------------------
# TAX
# ---------------------------
def test_tax(account_id):
    r = client.post("/taxes", json={
        "tax_name": "GST",
        "tax_rate": 18,
        "account_id": account_id
    })
    assert_ok(r, "Create Tax")
    return r.json()["tax_id"]

# ---------------------------
# VENDOR
# ---------------------------
def test_vendor():
    r = client.post("/vendors", json={
        "vendor_name": "ABC Medical Suppliers",
        "contact_info": "9876543210",
        "gst_number": "GSTIN123"
    })
    assert_ok(r, "Create Vendor")
    return r.json()["vendor_id"]

# ---------------------------
# BILL + BILL LINE
# ---------------------------
def test_bill(vendor_id, expense_account_id):
    r = client.post("/bills", json={
        "vendor_id": vendor_id,
        "bill_date": "2026-01-01",
        "total_amount": 5000,
        "tax_amount": 500,
        "status": "OPEN"
    })
    assert_ok(r, "Create Bill")
    bill_id = r.json()["bill_id"]

    r = client.post("/bill-lines", json={
        "bill_id": bill_id,
        "expense_account_id": expense_account_id,
        "description": "Medicines purchase",
        "amount": 5000
    })
    assert_ok(r, "Create Bill Line")

# ---------------------------
# INVOICE + INVOICE LINE
# ---------------------------
def test_invoice(patient_id, revenue_account_id):
    r = client.post("/invoices", json={
        "patient_id": patient_id,
        "invoice_date": "2026-01-01",
        "total_amount": 2000,
        "tax_amount": 200,
        "discount_amount": 0,
        "status": "ISSUED"
    })
    assert_ok(r, "Create Invoice")
    invoice_id = r.json()["invoice_id"]

    r = client.post("/invoice-lines", json={
        "invoice_id": invoice_id,
        "service_name": "Consultation",
        "account_id": revenue_account_id,
        "quantity": 1,
        "unit_price": 2000,
        "line_total": 2000
    })
    assert_ok(r, "Create Invoice Line")

    return invoice_id

# ---------------------------
# PAYMENT (AUTO JOURNAL POSTING)
# ---------------------------
def test_payment(invoice_id, bank_account_id):
    r = client.post("/payments", json={
        "invoice_id": invoice_id,
        "payment_date": "2026-01-01",
        "amount_paid": 2000,
        "payment_mode": "CASH",
        "bank_account_id": bank_account_id
    })
    assert_ok(r, "Create Payment")

# ---------------------------
# JOURNAL CHECK
# ---------------------------
def test_journal_entries():
    r = client.get("/journal-entries")
    assert_ok(r, "Get Journal Entries")

    entries = r.json()
    if len(entries) == 0:
        raise Exception(" No journal entries created")
    print(f" Journal entries count: {len(entries)}")

# ---------------------------
# MAIN TEST RUNNER
# ---------------------------
if __name__ == "__main__":
    print("\n🚀 Starting Finance Route Tests\n")

    # Setup master accounts
    cash_account = test_account()
    revenue_account = test_account()

    # Tax
    test_tax(cash_account)

    # Vendor & Bill
    vendor_id = test_vendor()
    test_bill(vendor_id, cash_account)

    # Invoice & Payment
    # NOTE: patient_id must exist in Patient module DB
    PATIENT_ID = 1
    BANK_ACCOUNT_ID = 1

    invoice_id = test_invoice(PATIENT_ID, revenue_account)
    test_payment(invoice_id, BANK_ACCOUNT_ID)

    # Journal verification
    test_journal_entries()

    print("\n ALL FINANCE ROUTES WORKING PERFECTLY ")
