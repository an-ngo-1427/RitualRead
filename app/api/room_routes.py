from flask_socketio import join_room,leave_room
from flask import Blueprint,render_template,request,session,redirect,url_for
from flask_login import login_required,current_user
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
@login_required
@room_routes.route('/<int:roomId>',methods=['GET','POST'])
def roomDetail(roomId):
    # need to check if the user is a member of the room!!!!!
    room = rooms[roomId]
    print('this is member----:',current_user.username)
    print('this is room-----',roomId,room)
    if not room:
        print('there is no room------')
        return redirect(url_for('not_found'))

    if request.method == 'GET':
        return render_template('room.html',room=room)
    else:
        username = current_user.username
        # if username not in room['members']:
        #     room['members'].append(username)
        session['room'] = roomId
        session['room_name'] = room['name']
        return render_template('room.html',room=room)

@login_required
@room_routes.route('/<int:roomId>',methods=['DELETE'])
def leaveRoom(roomId):
    userName = current_user.username
    print('entered leaving room----',userName)
    room = rooms.get(roomId)
    if not room:
        return

    session.pop('room',None)
    session.pop('room_name',None)
    return redirect(url_for('lobby.getLobby'))

@login_required
@room_routes.route('/',methods=['POST','GET'])
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

    roomCode = gen_code_room()
    # Initialize members as a set
    rooms[roomCode] = {'roomId': roomCode, 'name': name, 'members': set(), 'messages': []}
    session['room'] = roomCode
    session['room_name'] = name
    newRoom = rooms[roomCode]
    return {'room':newRoom}, 201
# create a function to delete a room
