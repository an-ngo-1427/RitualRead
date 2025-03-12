from flask_socketio import SocketIO,leave_room,join_room,send
from flask import session,request,redirect,url_for
from flask_login import current_user
from .api.room_routes import rooms
import os

origins = os.environ.get('PRO_ORIGIN') if os.environ.get('FLASK_ENV')=='production' else os.environ.get('DEV_ORIGIN')

sio = SocketIO(cors_allowed_origins = origins,debug=True)

@sio.on('connect')
def connect(auth):
    room = session.get('room')
    roomName = session.get('room_name')
    print('this  is room----',room)
    print('this is rooms-----',rooms)

    if not current_user.is_authenticated:
        print('not authenticated')
        return redirect(url_for('homePage'))
    if not room or not roomName:
        return
    if room not in rooms:
        print('left room')
        leave_room(room)

    # userName = session.get('username')
    userName = current_user.username
    join_room(room)

    rooms[room]['members'].append(userName)
    send(f"{userName} joined room",to=room)

@sio.on('message')
def message(message):
    print('message from client',message)
    send('this is message from server')

@sio.on('disconnect')
def disconnect():
    if not current_user.is_authenticated:
        return
    room = session.get('room')
    leave_room(room)
    send(f"{current_user.username} left the room")
    session.pop('room',None)
    session.pop('room_name',None)

@sio.on('start_game')
def startGame(data):
    print('---------starting game',data.get('players'))
