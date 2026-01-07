from database import db

class Vendor(db.Model):
    __tablename__ = "vendor"

    vendor_id = db.Column(db.Integer, primary_key=True)
    vendor_name = db.Column(db.String(255), nullable=False)
    contact_info = db.Column(db.String(255))
    gst_number = db.Column(db.String(50))

    bills = db.relationship("Bill", backref="vendor", lazy=True)

    def to_dict(self):
        return {
            "vendor_id": self.vendor_id,
            "vendor_name": self.vendor_name,
            "contact_info": self.contact_info,
            "gst_number": self.gst_number,
        }