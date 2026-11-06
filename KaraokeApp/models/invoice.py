from datetime import datetime
from extensions import db

class Invoice(db.Model):
    __tablename__ = "invoices"
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), unique=True, nullable=False)
    room_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    service_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    discount_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    vat_rate = db.Column(db.Numeric(5, 2), nullable=False, default=10)
    vat_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    total_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    status = db.Column(db.String(30), nullable=False, default="unpaid")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    booking = db.relationship("Booking", backref=db.backref("invoice", uselist=False))
