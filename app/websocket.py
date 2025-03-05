from flask_socketio import SocketIO,leave_room,join_room,send
from flask import session
from flask_login import current_user
from .api.room_routes import rooms
import os

origins = os.environ.get('PRO_ORIGIN') if os.environ.get('FLASK_ENV')=='production' else os.environ.get('DEV_ORIGIN')

sio = SocketIO(cors_allowed_origins = origins,debug=True)

@sio.on('connect')
def connect():
    room = session.get('room')
    roomName = session.get('room_name')
    if not room or not roomName:
        return
    if room not in rooms:
        leave_room(room)

    join_room(room)
    print('this  is room----',room)
    print('this is rooms',rooms)
    rooms[room]['members']+= 1
    print('current user-------',current_user.username)
    send('a user joined room',to=room)
@sio.on('message')
def message(message):
    print('message from client',message)
    send('this is message from server')
