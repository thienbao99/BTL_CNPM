from datetime import datetime
from extensions import db


class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def active_loyalty_card(self):
        """Trả về thẻ thân thiết đang hoạt động (nếu có)."""
        for card in self.loyalty_cards:
            if card.is_active:
                return card
        return None

    @property
    def is_vip(self):
        """Kiểm tra khách hàng có đang sở hữu thẻ VIP hoạt động hay không."""
        return self.active_loyalty_card is not None
