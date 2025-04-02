from flask_socketio import join_room,leave_room
from flask import Blueprint,render_template,request,session,redirect,url_for
from flask_login import current_user,login_required
from app.models import Room,db
import random
room_routes = Blueprint('rooms',__name__)
rooms={}
uniqueNames = set()

def gen_code_room():
    while(True):
        roomCode = random.randint(100000, 999999)
        if roomCode not in rooms:
            return roomCode


# getting room details and joining a room
@room_routes.route('/<int:roomId>',methods=['GET'])
@login_required
def roomDetail(roomId):
    room = Room.query.get(roomId)
    if not room:
        return {'errors':['room does not exist']}, 400
    return {'room':room.to_dict()},200


@room_routes.route('/',methods=['GET'])
@login_required
def getRooms():
    resRooms = Room.query.all()
    return {'rooms':[room.to_dict() for room in resRooms]},200

@room_routes.route('/<int:roomId>',methods=['POST'])
@login_required
def joinRoom(roomId):
    room = Room.query.get(roomId)
    if not room:
        return {'errors':['room does not exist']}, 400
    session['room'] = roomId
    session['room_name'] = room.name
    return {'room':room.to_dict()}, 200

@room_routes.route('/<int:roomId>',methods=['DELETE'])
@login_required
def leaveRoom(roomId):
    room = Room.query.get(roomId)
    if not room:
        return {'errors':['room does not exist']}, 400
    return {'message':'left room'}, 200

@room_routes.route('/',methods=['POST'])
@login_required
def createRoom():
    name = request.form.get("name")
    if not name:
        return {'errors':['please provide room name']}, 400
    if Room.query.filter_by(name=name).first():
        return {'errors':['room name already exists']}, 400


    newRoom = Room(name=name)
    db.session.add(newRoom)
    db.session.commit()
    session['room'] = newRoom.id
    session['room_name'] = newRoom.name
    return {'room':newRoom.to_dict()}, 201
# create a function to delete a room
