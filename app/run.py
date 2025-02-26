from app import flask_app,sio

if __name__ == '__main__':
    sio.run(flask_app,debug=True)
