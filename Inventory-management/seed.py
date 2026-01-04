from database import SessionLocal
from category.category_models import Category
from supplier.supplier_models import Supplier
from store_location.store_location_models import StoreLocation
from item.item_models import Item, ItemStatus
from departments.models import Department

db = SessionLocal()

# ------------------ DEPARTMENTS ------------------
departments = [
    Department(name="ICU"),
    Department(name="Pharmacy"),
    Department(name="Ward"),
]
db.add_all(departments)
db.commit()

# ------------------ CATEGORIES ------------------
categories = [
    Category(name="Gloves", description="Medical gloves"),
    Category(name="Syringes", description="Disposable syringes"),
    Category(name="Medicines", description="Hospital medicines"),
]
db.add_all(categories)
db.commit()

# ------------------ SUPPLIERS ------------------
suppliers = [
    Supplier(name="ABC Medicals", phone="9876543210"),
    Supplier(name="HealthCare Pvt Ltd", phone="9123456789"),
]
db.add_all(suppliers)
db.commit()

# ------------------ STORE LOCATIONS ------------------
locations = [
    StoreLocation(name="Main Store", location_type="Main"),
    StoreLocation(name="ICU Store", location_type="Department"),
]
db.add_all(locations)
db.commit()

# ------------------ ITEMS ------------------
items = [
    Item(
        code="GLV001",
        name="Surgical Gloves",
        unit="Box",
        unit_price=250,
        minimum_stock_level=10,
        expiry_applicable=False,
        category_id=categories[0].id,
        status=ItemStatus.active,
    ),
    Item(
        code="SYR001",
        name="Disposable Syringe",
        unit="Piece",
        unit_price=5,
        minimum_stock_level=100,
        expiry_applicable=False,
        category_id=categories[1].id,
        status=ItemStatus.active,
    ),
]

db.add_all(items)
db.commit()

db.close()
print("✅ Seed data inserted successfully")
