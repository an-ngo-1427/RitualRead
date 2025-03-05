from flask_socketio import SocketIO,leave_room,join_room,send
from flask import session,request
from flask_login import current_user
from .api.room_routes import rooms
import os

origins = os.environ.get('PRO_ORIGIN') if os.environ.get('FLASK_ENV')=='production' else os.environ.get('DEV_ORIGIN')

sio = SocketIO(cors_allowed_origins = origins,debug=True)

@sio.on('connect')
def connect(auth):
    room = session.get('room')
    roomName = session.get('room_name')

    if not current_user.is_authenticated:
        return
    if not room or not roomName:
        return
    if room not in rooms:
        leave_room(room)

    # userName = session.get('username')
    userName = current_user.username
    join_room(room)
    print('this  is room----',room)

    rooms[room]['members'].append(userName)
    print('this is rooms-----',rooms)
    send(f"{userName} joined room",to=room)
@sio.on('message')
def message(message):
    print('message from client',message)
    send('this is message from server')
