from flask import Blueprint, render_template
from sqlalchemy import func
from models import Invoice, Booking, Room

report_bp = Blueprint("report", __name__, url_prefix="/reports")

@report_bp.route("/")
def index():
    rows = (
        Invoice.query.join(Booking, Invoice.booking_id == Booking.id)
        .join(Room, Booking.room_id == Room.id)
        .filter(Invoice.status == "paid")
        .with_entities(Room.room_name, func.sum(Invoice.total_amount).label("revenue"))
        .group_by(Room.id, Room.room_name).all()
    )
    return render_template("report/index.html", rows=rows)
