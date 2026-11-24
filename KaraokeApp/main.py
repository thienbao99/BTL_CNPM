from flask import Flask, redirect, url_for
from config import Config
from extensions import db
from controllers import init_routes

def create_app():
    app = Flask(__name__, template_folder="views", static_folder="static")
    app.config.from_object(Config)
    db.init_app(app)

    # Đăng ký toàn bộ route thuần Flask
    init_routes(app)

    with app.app_context():
        from models import User, Room, Booking, Service, BookingService, Invoice, Customer, LoyaltyCard
        db.create_all()

        # Nạp dữ liệu mẫu ban đầu nếu bảng phòng chưa có dữ liệu
        if Room.query.count() == 0:
            import json
            from pathlib import Path
            data_dir = Path(__file__).resolve().parent / "data"

            rooms_file = data_dir / "rooms.json"
            if rooms_file.exists():
                with open(rooms_file, "r", encoding="utf-8") as f:
                    for item in json.load(f):
                        db.session.add(Room(**item))

            services_file = data_dir / "services.json"
            if services_file.exists():
                with open(services_file, "r", encoding="utf-8") as f:
                    for item in json.load(f):
                        db.session.add(Service(**item))

            customers_file = data_dir / "customers.json"
            if customers_file.exists():
                with open(customers_file, "r", encoding="utf-8") as f:
                    for item in json.load(f):
                        db.session.add(Customer(**item))

            db.session.commit()

    @app.route("/")
    def home():
        return redirect(url_for("room_index"))

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
