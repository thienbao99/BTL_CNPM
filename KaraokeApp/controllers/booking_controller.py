from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, jsonify
from extensions import db
from models import Booking, Room, Customer

def init_booking_routes(app):
    @app.route("/bookings/")
    def booking_index():
        bookings = Booking.query.order_by(Booking.start_time.desc()).all()
        return render_template("booking/index.html", bookings=bookings)

    @app.route("/bookings/api/lookup-customer")
    def booking_lookup_customer():
        """API tra cứu thông tin khách hàng nhanh qua số điện thoại."""
        phone = request.args.get("phone", "").strip()
        if not phone or len(phone) < 9:
            return jsonify({"found": False, "message": "Số điện thoại chưa đủ ký tự"})

        customer = Customer.query.filter_by(phone=phone).first()
        if not customer:
            return jsonify({"found": False})

        active_card = customer.active_loyalty_card
        return jsonify({
            "found": True,
            "id": customer.id,
            "full_name": customer.full_name,
            "phone": customer.phone,
            "email": customer.email or "",
            "is_vip": bool(active_card),
            "card_code": active_card.card_code if active_card else None,
            "discount_percent": float(active_card.discount_percent) if active_card else 0.0,
            "booking_count": len(customer.bookings)
        })

    @app.route("/bookings/create", methods=["GET", "POST"])
    def booking_create():
        rooms = Room.query.order_by(Room.room_name).all()
        if request.method == "POST":
            try:
                room_id = int(request.form["room_id"])
                guest_count = int(request.form["guest_count"])
                start_time = datetime.fromisoformat(request.form["start_time"])
                end_time = datetime.fromisoformat(request.form["end_time"])
                customer_name = request.form["customer_name"].strip()
                customer_phone = request.form.get("customer_phone", "").strip()

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

                # Ràng buộc: Kiểm tra số điện thoại thành viên
                customer_id = None
                if customer_phone:
                    customer = Customer.query.filter_by(phone=customer_phone).first()
                    if customer:
                        customer_name = customer.full_name
                        customer_id = customer.id
                    else:
                        if not customer_name:
                            raise ValueError("Vui lòng nhập họ tên cho khách hàng mới.")
                        customer = Customer(full_name=customer_name, phone=customer_phone)
                        db.session.add(customer)
                        db.session.flush()
                        customer_id = customer.id

                booking = Booking(
                    room_id=room_id,
                    customer_id=customer_id,
                    customer_name=customer_name,
                    customer_phone=customer_phone,
                    guest_count=guest_count,
                    start_time=start_time,
                    end_time=end_time
                )
                db.session.add(booking)
                db.session.commit()
                flash(f"Đặt phòng thành công cho khách hàng '{customer_name}'.", "success")
                return redirect(url_for("booking_index"))
            except (ValueError, KeyError) as exc:
                db.session.rollback()
                flash(str(exc) or "Dữ liệu đặt phòng không hợp lệ.", "danger")

        prefill_room_id = request.args.get("room_id", type=int)
        prefill_phone = request.args.get("phone", "")
        prefill_name = request.args.get("name", "")

        return render_template(
            "booking/create.html",
            rooms=rooms,
            prefill_room_id=prefill_room_id,
            prefill_phone=prefill_phone,
            prefill_name=prefill_name
        )
