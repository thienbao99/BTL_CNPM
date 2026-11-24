from .auth_controller import init_auth_routes
from .room_controller import init_room_routes
from .booking_controller import init_booking_routes
from .service_controller import init_service_routes
from .payment_controller import init_payment_routes
from .report_controller import init_report_routes
from .customer_controller import init_customer_routes

def init_routes(app):
    init_auth_routes(app)
    init_room_routes(app)
    init_booking_routes(app)
    init_service_routes(app)
    init_payment_routes(app)
    init_report_routes(app)
    init_customer_routes(app)
