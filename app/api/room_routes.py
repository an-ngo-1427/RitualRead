from flask import Blueprint,render_template,request,session
from flask_socketio import join_room,leave_room
import random
room_routes = Blueprint('rooms',__name__)
rooms={}
uniqueNames = set()

def gen_code_room():
    while(True):
        roomCode = random.randint(100000, 999999)
        if roomCode not in rooms:
            return roomCode

    rooms[roomCode] = {'name':'string','members':0,'messages':[]}

@room_routes.route('/',methods=['POST','GET'])
def createRoom():
    errors = []
    if request.method == 'GET':
        return render_template('roomForm.html')

    form = request.form
    name = request.form.get("name")
    # checking if name is entered
    if not name:
        errors.append('enter room name')
        return render_template('roomForm.html',errors=errors)

    # checking if given name is unique
    if name in uniqueNames:
        errors.append('name already exists')
        return render_template('roomForm.html',form=form,errors=errors)
    else:
        uniqueNames.add(name)

    roomCode = gen_code_room()
    rooms[roomCode] = {'name':name,'members':0,'messages':[]}
    session['room'] = roomCode
    session['room_name'] = name
    return render_template('room.html',room=rooms[roomCode])
