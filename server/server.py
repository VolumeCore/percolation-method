import os

from flask import Flask, render_template, request, json
from flask_socketio import SocketIO, emit
from matrix import Matrix
from hoshenKopelman import HoshenKopelman
from dijkstra import Dijkstra

project_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
client_dir = os.path.join(project_dir, 'client')
static_dir = os.path.join(client_dir, 'static')
template_dir = os.path.join(client_dir, 'templates')
app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
socketio = SocketIO(app, manage_session=False)


@app.route("/")
def hello():
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


@app.route("/crossMatrix/<int:size>/<int:concentration>", methods=['GET'])
def cross_matrix(concentration, size):
    return Matrix(concentration, size).cross_matrix()


@app.route("/shortest", methods=['POST'])
def shortestWay():
    data = json.loads(request.data)
    matrix = data['matrix']
    minLenght = float('inf')
    res = []
    for i in range(len(matrix[0])):
        for j in range(len(matrix[0])):
            path, cost = Dijkstra(matrix, (0, i), (len(matrix) - 1, j)).method()
            if cost < minLenght:
                res = path
                minLenght = cost

    return {'path': res, 'cost': minLenght}


@app.route("/verticalZebraMatrix/<int:size>/<int:concentration>", methods=['GET'])
def vertical_zebra_matrix(concentration, size):
    return Matrix(concentration, size).vertical_zebra_matrix()


@app.route("/horizontalZebraMatrix/<int:size>/<int:concentration>", methods=['GET'])
def horizontal_zebra_matrix(concentration, size):
    return Matrix(concentration, size).horizontal_zebra_matrix()


@app.route("/verticalRainMatrix/<int:size>/<int:concentration>", methods=['GET'])
def vertical_rain_matrix(concentration, size):
    return Matrix(concentration, size).vertical_rain_matrix()


@app.route("/horizontalRainMatrix/<int:size>/<int:concentration>", methods=['GET'])
def horizontal_rain_matrix(concentration, size):
    return Matrix(concentration, size).horizontal_rain_matrix()


@app.route("/chessMatrix/<int:size>/<int:concentration>", methods=['GET'])
def chess_matrix(concentration, size):
    return Matrix(concentration, size).chess_matrix()


@app.route("/circlesMatrix/<int:size>/<int:concentration>", methods=['GET'])
def circles_matrix(concentration, size):
    return Matrix(concentration, size).circles_matrix()


@app.route("/hMatrix/<int:size>/<int:concentration>", methods=['GET'])
def H_matrix(concentration, size):
    return Matrix(concentration, size).H_matrix()


@app.route("/hShiftMatrix/<int:size>/<int:concentration>", methods=['GET'])
def H_shift_matrix(concentration, size):
    return Matrix(concentration, size).H_shift_matrix()


@socketio.on('hoshen_kopelman', namespace='/app')
def hoshen_kopelman(message):
    print("Start Hoshen Kopelman")
    HoshenKopelman(json.loads(message['matrix'])).method()


@socketio.on("dijkstra", namespace='/app')
def dijkstra(message):
    start = (message['x1'], message['y1'])
    end = (message['x2'], message['y2'])
    matrix = json.loads(message['matrix'])
    result, cost = Dijkstra(matrix, start, end).method()

    if result is None:
        emit('dijkstra', {'path': [], 'cost': 0})
    else:
        emit('dijkstra', {'path': result, 'cost': cost})


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=4567, allow_unsafe_werkzeug=True)
