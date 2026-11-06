from flask import Blueprint, render_template
from models import Invoice

payment_bp = Blueprint("payment", __name__, url_prefix="/payments")

@payment_bp.route("/")
def index():
    invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
    return render_template("payment/invoice.html", invoices=invoices)
