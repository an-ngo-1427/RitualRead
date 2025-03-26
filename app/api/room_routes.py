from flask_socketio import join_room,leave_room
from flask import Blueprint,render_template,request,session,redirect,url_for
from flask_login import current_user,login_required
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
@room_routes.route('/<int:roomId>',methods=['GET','POST'])
@login_required
def roomDetail(roomId):
    # need to check if the user is a member of the room!!!!!
    room = rooms[roomId]
    print('this is room-----',roomId,room)
    if not room:
        print('there is no room------')
        return redirect(url_for('not_found'))

    if request.method == 'GET':
        return render_template('room.html',room=room)
    else:
        session['room'] = roomId
        session['room_name'] = room['name']
        return render_template('room.html',room=room)

@room_routes.route('/',methods=['GET'])
@login_required
def getRooms():
    resRooms = [{'roomId':room['roomId'],'name':room['name'],'members':list(room['members'])} for room in rooms.values()]
    return {'rooms':resRooms},200

@room_routes.route('/<int:roomId>',methods=['DELETE'])
@login_required
def leaveRoom(roomId):
    room = rooms.get(roomId)
    if not room:
        return

    session.pop('room',None)
    session.pop('room_name',None)
    return redirect(url_for('lobby.getLobby'))

@room_routes.route('/',methods=['POST'])
@login_required
def createRoom():
    form = request.form
    name = request.form.get("name")

    print(name)
    if not name:
        return {'errors':['please provide room name']}, 400
    if name in uniqueNames:
        return {'errors':['room name already exists']}, 400
    else:
        uniqueNames.add(name)
    if(current_user.is_authenticated):
        print('this is current user----room',current_user)
    roomCode = gen_code_room()
    # Initialize members as a set
    rooms[roomCode] = {'roomId': roomCode, 'name': name, 'members': set(), 'messages': []}
    session['room'] = roomCode
    session['room_name'] = name
    newRoom = {**rooms[roomCode], 'members': list(rooms[roomCode]['members'])}
    return {'room':newRoom}, 201
# create a function to delete a room
