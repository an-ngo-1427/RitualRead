from flask_socketio import SocketIO,leave_room,join_room,send
from flask import session,request,redirect,url_for
from flask_login import current_user
from .api.room_routes import rooms
import os

origins = os.environ.get('PRO_ORIGIN') if os.environ.get('FLASK_ENV')=='production' else os.environ.get('DEV_ORIGIN')

sio = SocketIO(cors_allowed_origins = origins,debug=True,logger=True, engineio_logger=True)

@sio.on('connect_error')
def connect_error(err):
    print('error connecting',err)
@sio.on('connect')
def connect(auth):
    roomCode = session.get('room')
    roomName = session.get('room_name')
    print('this is room code',roomCode)
    print('this  is room----',rooms[roomCode])
    print('this is rooms-----',rooms)

    if not current_user.is_authenticated:
        return redirect(url_for('homePage'))
    if not roomCode or not roomName:
        return
    if roomCode not in rooms:
        print('left room')
        leave_room(roomCode)

    # userName = session.get('username')
    room = rooms.get(roomCode)
    userName = current_user.username
    print('this is username---',userName)
    join_room(roomCode)
    room['members'].add(userName)
    send(f"{userName} joined room")

@sio.on('message')
def message(message):
    print('message from client',message)
    send('this is message from server')

@sio.on('disconnect')
def disconnect(*arg):
    print('disconnecting from server',current_user.username)
    if not current_user.is_authenticated:
        return

    userName = current_user.username
    roomId = session.get('room')
    room = rooms.get(roomId)

    if not room:
        return
    room['members'].discard(userName)
    print('this is disconnection-----',rooms)
    leave_room(roomId)
    send(f"{current_user.username} left the room",to=roomId)
    session.pop('room',None)
    session.pop('room_name',None)

@sio.on('start_game')
def startGame(data):
    print('---------starting game',data.get('players'))
