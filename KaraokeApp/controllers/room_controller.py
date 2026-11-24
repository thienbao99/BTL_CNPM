from flask import render_template
from models import Room

def init_room_routes(app):
    @app.route("/rooms/")
    def room_index():
        rooms = Room.query.all()
        return render_template("room/index.html", rooms=rooms)

    @app.route("/rooms/<int:room_id>")
    def room_detail(room_id):
        room = Room.query.get_or_404(room_id)
        return render_template("room/detail.html", room=room)
