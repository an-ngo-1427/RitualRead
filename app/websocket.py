from flask_socketio import SocketIO,leave_room,join_room,send,emit
from flask import session,request,redirect,url_for
from flask_login import current_user
from app.models import Room,User
from app.models import db
import os

origins = os.environ.get('PRO_ORIGIN') if os.environ.get('FLASK_ENV')=='production' else os.environ.get('DEV_ORIGIN')

sio = SocketIO(cors_allowed_origins = origins,debug=True,logger=True, engineio_logger=True)

@sio.on('connect_error')
def connect_error(err):
    print('error connecting',err)
@sio.on('connect')
def connect(auth):
    roomId = session.get('room')
    roomName = session.get('room_name')
    room = Room.query.filter_by(id = roomId, name = roomName).first()
    user = User.query.get(current_user.id)

    if not room:
        session.pop('room',None)
        session.pop('room_name',None)
        leave_room(roomId)
    user.room_id = roomId
    db.session.commit()
    join_room(roomId)

    send(f"{user.username} joined room")
    emit("join_room",{'room':room.to_dict()},to=roomId)
    emit('room','data')

@sio.on('message')
def message(message):
    print('message from client',message)
    send('this is message from server')

@sio.on('disconnect')
def disconnect(*arg):
    print('disconnecting from server----------',current_user.username)
    if not current_user.is_authenticated:
        return

    roomId = session.get('room')

    if not roomId:
        return
    # delete user from room
    current_user.room_id = None
    # if members of room is empty, delete room
    room = Room.query.get(roomId)
    roomMembers = room.members
    leave_room(roomId)

    if not roomMembers:
        db.session.delete(room)

    db.session.commit()
    emit('leave_room',{'room':room.to_dict()},to=roomId)
    session.pop('room',None)
    session.pop('room_name',None)

@sio.on('start_game')
def startGame(data):
    print('---------starting game',data.get('players'))
