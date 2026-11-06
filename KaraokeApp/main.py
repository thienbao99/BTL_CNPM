from flask import Flask, redirect, url_for
from config import Config
from extensions import db
from controllers import register_blueprints

def create_app():
    app = Flask(__name__, template_folder="views", static_folder="static")
    app.config.from_object(Config)
    db.init_app(app)
    register_blueprints(app)

    with app.app_context():
        from models import User, Room, Booking, Service, BookingService, Invoice, Customer, LoyaltyCard
        db.create_all()

    @app.route("/")
    def home():
        return redirect(url_for("room.index"))

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
