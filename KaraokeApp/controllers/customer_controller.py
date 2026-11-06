from flask import Blueprint, render_template
from models import Customer, LoyaltyCard

customer_bp = Blueprint("customer", __name__, url_prefix="/customers")

@customer_bp.route("/")
def index():
    customers = Customer.query.order_by(Customer.full_name).all()
    return render_template("customer/index.html", customers=customers)

@customer_bp.route("/loyalty")
def loyalty():
    cards = LoyaltyCard.query.order_by(LoyaltyCard.issued_at.desc()).all()
    return render_template("customer/loyalty.html", cards=cards)
