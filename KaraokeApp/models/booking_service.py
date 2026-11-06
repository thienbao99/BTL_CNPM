from extensions import db

class BookingService(db.Model):
    __tablename__ = "booking_services"
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(12, 2), nullable=False)
    booking = db.relationship("Booking", backref="ordered_services")
    service = db.relationship("Service")
