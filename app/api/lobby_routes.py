from flask import Blueprint, render_template
from .room_routes import rooms

lobby_routes = Blueprint('lobby',__name__)

@lobby_routes.route('/',methods=['GET'])
def getLobby():
    return render_template('lobby.html',rooms=rooms)
