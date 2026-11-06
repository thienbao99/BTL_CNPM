from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Booking, Room

booking_bp = Blueprint("booking", __name__, url_prefix="/bookings")

@booking_bp.route("/")
def index():
    bookings = Booking.query.order_by(Booking.start_time.desc()).all()
    return render_template("booking/index.html", bookings=bookings)

@booking_bp.route("/create", methods=["GET", "POST"])
def create():
    rooms = Room.query.order_by(Room.room_name).all()
    if request.method == "POST":
        try:
            room_id = int(request.form["room_id"])
            guest_count = int(request.form["guest_count"])
            start_time = datetime.fromisoformat(request.form["start_time"])
            end_time = datetime.fromisoformat(request.form["end_time"])
            room = Room.query.get_or_404(room_id)

            if not 1 <= guest_count <= min(15, room.capacity):
                raise ValueError("Số khách phải từ 1 đến tối đa 15 người và không vượt sức chứa phòng.")
            if end_time <= start_time:
                raise ValueError("Giờ kết thúc phải sau giờ bắt đầu.")

            overlap = Booking.query.filter(
                Booking.room_id == room_id,
                Booking.status != "cancelled",
                Booking.start_time < end_time,
                Booking.end_time > start_time
            ).first()
            if overlap:
                raise ValueError("Phòng đã có lịch đặt trùng khung giờ.")

            booking = Booking(
                room_id=room_id,
                customer_name=request.form["customer_name"].strip(),
                customer_phone=request.form.get("customer_phone", "").strip(),
                guest_count=guest_count,
                start_time=start_time,
                end_time=end_time
            )
            db.session.add(booking)
            db.session.commit()
            flash("Đặt phòng thành công.", "success")
            return redirect(url_for("booking.index"))
        except (ValueError, KeyError) as exc:
            db.session.rollback()
            flash(str(exc) or "Dữ liệu đặt phòng không hợp lệ.", "danger")
    return render_template("booking/create.html", rooms=rooms)
