from .auth_controller import auth_bp
from .room_controller import room_bp
from .booking_controller import booking_bp
from .service_controller import service_bp
from .payment_controller import payment_bp
from .report_controller import report_bp
from .customer_controller import customer_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(customer_bp)
