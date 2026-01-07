from database import SessionLocal
from account.account_models import Account

db = SessionLocal()

acc = Account(
    account_name="Test Bank",
    account_type="Asset"
)

db.add(acc)
db.commit()
db.refresh(acc)

print("Inserted Account ID:", acc.account_id)
