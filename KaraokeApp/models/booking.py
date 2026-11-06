from datetime import datetime
from extensions import db

class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    customer_name = db.Column(db.String(120), nullable=False)
    customer_phone = db.Column(db.String(30))
    guest_count = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(30), nullable=False, default="booked")
    room = db.relationship("Room", backref="bookings")
    customer = db.relationship("Customer", backref="bookings")
