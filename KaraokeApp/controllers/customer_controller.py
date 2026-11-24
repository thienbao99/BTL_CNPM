import re
import secrets
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from extensions import db
from models import Customer, LoyaltyCard, Booking

def is_valid_phone(phone: str) -> bool:
    """Kiểm tra số điện thoại (9-12 chữ số)."""
    return bool(re.match(r"^[0-9]{9,12}$", phone))

def init_customer_routes(app):
    @app.route("/customers/")
    def customer_index():
        q = request.args.get("q", "").strip()
        query = Customer.query
        if q:
            query = query.filter(
                (Customer.full_name.ilike(f"%{q}%")) | (Customer.phone.ilike(f"%{q}%"))
            )
        customers = query.order_by(Customer.id.desc()).all()
        return render_template("customer/index.html", customers=customers, search_query=q)

    @app.route("/customers/create", methods=["POST"])
    def customer_create():
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()

        if not full_name:
            flash("Vui lòng nhập họ tên khách hàng.", "danger")
            return redirect(url_for("customer_index"))

        if not phone or not is_valid_phone(phone):
            flash("Số điện thoại không hợp lệ (phải từ 9-12 số).", "danger")
            return redirect(url_for("customer_index"))

        existing = Customer.query.filter_by(phone=phone).first()
        if existing:
            flash(f"Số điện thoại {phone} đã tồn tại cho khách hàng '{existing.full_name}'.", "danger")
            return redirect(url_for("customer_index"))

        try:
            customer = Customer(
                full_name=full_name,
                phone=phone,
                email=email if email else None
            )
            db.session.add(customer)
            db.session.commit()
            flash(f"Thêm khách hàng '{full_name}' thành công!", "success")
        except Exception as exc:
            db.session.rollback()
            flash(f"Lỗi khi thêm khách hàng: {exc}", "danger")

        return redirect(url_for("customer_index"))

    @app.route("/customers/<int:customer_id>")
    def customer_detail(customer_id):
        customer = Customer.query.get_or_404(customer_id)

        # Thống kê lượt hát trong tháng hiện tại theo quy tắc nghiệp vụ
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        if now.month == 12:
            start_of_next_month = datetime(now.year + 1, 1, 1)
        else:
            start_of_next_month = datetime(now.year, now.month + 1, 1)

        monthly_bookings = Booking.query.filter(
            Booking.customer_id == customer_id,
            Booking.status != "cancelled",
            Booking.start_time >= start_of_month,
            Booking.start_time < start_of_next_month
        ).count()

        total_bookings = len(customer.bookings)
        active_loyalty = customer.active_loyalty_card
        is_eligible_for_loyalty = monthly_bookings >= 10 and not active_loyalty

        bookings = Booking.query.filter_by(customer_id=customer_id).order_by(Booking.start_time.desc()).all()

        return render_template(
            "customer/detail.html",
            customer=customer,
            total_bookings=total_bookings,
            monthly_bookings=monthly_bookings,
            active_loyalty=active_loyalty,
            is_eligible_for_loyalty=is_eligible_for_loyalty,
            bookings=bookings,
            current_month=f"{now.month}/{now.year}"
        )

    @app.route("/customers/<int:customer_id>/edit", methods=["GET", "POST"])
    def customer_edit(customer_id):
        customer = Customer.query.get_or_404(customer_id)
        if request.method == "POST":
            full_name = request.form.get("full_name", "").strip()
            phone = request.form.get("phone", "").strip()
            email = request.form.get("email", "").strip()

            if not full_name:
                flash("Vui lòng nhập họ tên khách hàng.", "danger")
                return render_template("customer/edit.html", customer=customer)

            if not phone or not is_valid_phone(phone):
                flash("Số điện thoại không hợp lệ (phải từ 9-12 số).", "danger")
                return render_template("customer/edit.html", customer=customer)

            existing = Customer.query.filter(Customer.phone == phone, Customer.id != customer_id).first()
            if existing:
                flash(f"Số điện thoại {phone} đã được sử dụng bởi khách hàng '{existing.full_name}'.", "danger")
                return render_template("customer/edit.html", customer=customer)

            try:
                customer.full_name = full_name
                customer.phone = phone
                customer.email = email if email else None
                db.session.commit()
                flash(f"Cập nhật thông tin khách hàng '{customer.full_name}' thành công!", "success")
                return redirect(url_for("customer_detail", customer_id=customer.id))
            except Exception as exc:
                db.session.rollback()
                flash(f"Lỗi khi cập nhật khách hàng: {exc}", "danger")

        return render_template("customer/edit.html", customer=customer)

    @app.route("/customers/<int:customer_id>/delete", methods=["POST"])
    def customer_delete(customer_id):
        customer = Customer.query.get_or_404(customer_id)

        if customer.bookings:
            flash(
                f"Không thể xóa khách hàng '{customer.full_name}' vì đã có {len(customer.bookings)} lịch đặt phòng trong hệ thống.",
                "warning"
            )
            return redirect(url_for("customer_index"))

        try:
            for card in customer.loyalty_cards:
                db.session.delete(card)
            db.session.delete(customer)
            db.session.commit()
            flash(f"Đã xóa khách hàng '{customer.full_name}' khỏi hệ thống.", "success")
        except Exception as exc:
            db.session.rollback()
            flash(f"Lỗi khi xóa khách hàng: {exc}", "danger")

        return redirect(url_for("customer_index"))

    @app.route("/customers/<int:customer_id>/issue-loyalty", methods=["POST"])
    def customer_issue_loyalty(customer_id):
        customer = Customer.query.get_or_404(customer_id)

        active_card = customer.active_loyalty_card
        if active_card:
            flash(f"Khách hàng '{customer.full_name}' đã sở hữu thẻ thân thiết ({active_card.card_code}).", "warning")
            return redirect(url_for("customer_detail", customer_id=customer_id))

        try:
            phone_suffix = customer.phone[-4:] if len(customer.phone) >= 4 else customer.phone
            rand_token = secrets.token_hex(2).upper()
            card_code = f"VIP-{phone_suffix}-{rand_token}"

            card = LoyaltyCard(
                customer_id=customer.id,
                card_code=card_code,
                discount_percent=5.0,
                is_active=True
            )
            db.session.add(card)
            db.session.commit()
            flash(f"Cấp thẻ khách hàng thân thiết thành công! Mã thẻ: {card_code} (Ưu đãi giảm 5%).", "success")
        except Exception as exc:
            db.session.rollback()
            flash(f"Lỗi khi cấp thẻ: {exc}", "danger")

        return redirect(url_for("customer_detail", customer_id=customer_id))

    @app.route("/customers/loyalty")
    def customer_loyalty():
        cards = LoyaltyCard.query.order_by(LoyaltyCard.issued_at.desc()).all()
        return render_template("customer/loyalty.html", cards=cards)

    @app.route("/customers/loyalty/<int:card_id>/toggle-status", methods=["POST"])
    def customer_toggle_loyalty_status(card_id):
        card = LoyaltyCard.query.get_or_404(card_id)
        try:
            card.is_active = not card.is_active
            db.session.commit()
            status_text = "kích hoạt" if card.is_active else "tạm ngừng hoạt động"
            flash(f"Đã chuyển thẻ {card.card_code} sang trạng thái {status_text}.", "success")
        except Exception as exc:
            db.session.rollback()
            flash(f"Lỗi khi cập nhật trạng thái thẻ: {exc}", "danger")

        redirect_to = request.form.get("redirect_to")
        if redirect_to == "detail":
            return redirect(url_for("customer_detail", customer_id=card.customer_id))
        return redirect(url_for("customer_loyalty"))
