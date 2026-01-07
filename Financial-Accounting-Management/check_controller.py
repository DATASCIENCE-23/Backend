from database import SessionLocal
from account.account_controller import AccountController
from account.account_schema import AccountCreate

db = SessionLocal()

# CREATE
acc = AccountController.create(
    db,
    AccountCreate(account_name="Test Cash", account_type="Asset")
)
print("Created:", acc.account_id)

# READ
fetched = AccountController.get(db, acc.account_id)
print("Fetched:", fetched.account_name)

# UPDATE
updated = AccountController.update(
    db,
    acc.account_id,
    {"account_name": "Updated Cash"}
)
print("Updated:", updated.account_name)

# DELETE
AccountController.delete(db, acc.account_id)
print("Deleted")
