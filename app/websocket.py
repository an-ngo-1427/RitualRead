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
    print('this is room code',room)
    print('this  is room----',rooms[room])
    print('this is rooms-----',rooms)

    if not current_user.is_authenticated:
        return redirect(url_for('homePage'))
    if not room or not roomName:
        return
    if room not in rooms:
        print('left room')
        leave_room(room)

    # userName = session.get('username')
    userName = current_user.username
    print('this is username---',userName)
    join_room(room)
    if(userName not in rooms[room]['members']):
        rooms[room]['members'].append(userName)

    send(f"{userName} joined room",to=room)

@sio.on('message')
def message(message):
    print('message from client',message)
    send('this is message from server')

@sio.on('disconnect')
def disconnect():
    print('disconnecting from server',current_user.username)
    if not current_user.is_authenticated:
        return

    userName = current_user.username
    roomId = session.get('room')
    room = rooms[roomId]
    for member in room['members']:
        if userName == member:
            member = None
            break
    print('this is disconnection-----',rooms)
    leave_room(roomId)
    send(f"{current_user.username} left the room",to=roomId)
    session.pop('room',None)
    session.pop('room_name',None)

@sio.on('start_game')
def startGame(data):
    print('---------starting game',data.get('players'))
