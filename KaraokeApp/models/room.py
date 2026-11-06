from extensions import db

class Room(db.Model):
    __tablename__ = "rooms"
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(80), unique=True, nullable=False)
    room_type = db.Column(db.String(50), default="Standard")
    capacity = db.Column(db.Integer, nullable=False, default=15)
    hourly_price = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    status = db.Column(db.String(30), nullable=False, default="available")
