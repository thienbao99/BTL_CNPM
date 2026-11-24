from flask import render_template
from models import Invoice

def init_payment_routes(app):
    @app.route("/payments/")
    def payment_index():
        invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
        return render_template("payment/invoice.html", invoices=invoices)
