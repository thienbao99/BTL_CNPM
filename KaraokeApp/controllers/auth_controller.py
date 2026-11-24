from flask import render_template

def init_auth_routes(app):
    @app.route("/auth/login")
    def auth_login():
        return render_template("auth/login.html")
