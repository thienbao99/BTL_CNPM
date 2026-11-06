from flask import Blueprint, render_template
from models import Service

service_bp = Blueprint("service", __name__, url_prefix="/services")

@service_bp.route("/")
def index():
    services = Service.query.order_by(Service.category, Service.service_name).all()
    return render_template("service/index.html", services=services)

@service_bp.route("/manage")
def manage():
    services = Service.query.order_by(Service.service_name).all()
    return render_template("service/manage.html", services=services)
