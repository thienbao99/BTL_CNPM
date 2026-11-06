from flask import Blueprint, render_template
from models import Room

room_bp = Blueprint("room", __name__, url_prefix="/rooms")


@room_bp.route("/")
def index():

    rooms = Room.query.all()

    return render_template(
        "room/index.html",
        rooms=rooms
    )