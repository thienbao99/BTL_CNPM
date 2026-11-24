from flask import render_template
from models import Service

def init_service_routes(app):
    @app.route("/services/")
    def service_index():
        services = Service.query.order_by(Service.category, Service.service_name).all()
        return render_template("service/index.html", services=services)

    @app.route("/services/manage")
    def service_manage():
        services = Service.query.order_by(Service.service_name).all()
        return render_template("service/manage.html", services=services)
