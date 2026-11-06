from datetime import datetime
from extensions import db

class LoyaltyCard(db.Model):
    __tablename__ = "loyalty_cards"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    card_code = db.Column(db.String(50), unique=True, nullable=False)
    discount_percent = db.Column(db.Numeric(5, 2), nullable=False, default=5)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    customer = db.relationship("Customer", backref="loyalty_cards")
