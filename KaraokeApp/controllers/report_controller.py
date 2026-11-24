from flask import render_template
from sqlalchemy import func
from models import Invoice, Booking, Room

def init_report_routes(app):
    @app.route("/reports/")
    def report_index():
        rows = (
            Invoice.query.join(Booking, Invoice.booking_id == Booking.id)
            .join(Room, Booking.room_id == Room.id)
            .filter(Invoice.status == "paid")
            .with_entities(Room.room_name, func.sum(Invoice.total_amount).label("revenue"))
            .group_by(Room.id, Room.room_name).all()
        )
        return render_template("report/index.html", rows=rows)
