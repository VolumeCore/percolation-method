import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from matrix import Matrix
from hoshenKopelman import HoshenKopelman

project_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
client_dir = os.path.join(project_dir, 'client')
static_dir = os.path.join(client_dir, 'static')
template_dir = os.path.join(client_dir, 'templates')
app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
socketio = SocketIO(app, manage_session=False)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect', namespace='/app')
def test_connect():
    print('Client Connect')


@socketio.on('disconnect', namespace='/app')
def test_disconnect():
    print('Client disconnected')


@app.route("/generateMatrix/<int:size>/<int:concentration>", methods=['GET'])
def generation_matrix(concentration, size):
    return Matrix(concentration, size).generation_matrix()


@socketio.on('hoshen_kopelman', namespace='/app')
def hoshen_kopelman(message):
    print("Start Hoshen Kopelman")
    HoshenKopelman(int(message['concentration']), int(message['size'])).random_matrix()


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=4567)
