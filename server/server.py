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
@app.route("/dijkstra", methods=['POST'])
def dijkstra_req():
    data = json.loads(request.data)
    start = (data['x1'], data['y1'])
    end = (data['x2'], data['y2'])
    matrix = data['matrix']
    result, cost = dijkstra(matrix, start, end)

    if result is None:
        return {'path': [], 'cost': 0}
    return {'path': result, 'cost': cost}


@app.route("/shortest", methods=['POST'])
def shortestWay():
    data = json.loads(request.data)
    matrix = data['matrix']
    minLenght = float('inf')
    res = []
    for i in range(len(matrix[0])):
        for j in range(len(matrix[0])):
            path, cost = dijkstra(matrix, (0, i), (len(matrix) - 1, j))
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
        emit('dijkstra', {'matrix': []})
    else:
        emit('dijkstra', {'matrix': result})


def dijkstra(matrix, start, end):
    # преобразуем матрицу в граф
    graph = {}
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        for j in range(cols):
            neighbors = []
            if i > 0:
                neighbors.append([(i - 1, j), 1 if matrix[i - 1][j] == 1 else len(matrix) ** 2 + 1])
            if i < rows - 1:
                neighbors.append([(i + 1, j), 1 if matrix[i + 1][j] == 1 else len(matrix) ** 2 + 1])
            if j > 0:
                neighbors.append([(i, j - 1), 1 if matrix[i][j - 1] == 1 else len(matrix) ** 2 + 1])
            if j < cols - 1:
                neighbors.append([(i, j + 1), 1 if matrix[i][j + 1] == 1 else len(matrix) ** 2 + 1])
            graph[(i, j)] = neighbors

    # инициализируем алгоритм Дейкстры
    queue = [(1 if matrix[start[0]][start[1]] == 1 else len(matrix) ** 2 + 1, start, [])]
    visited = set()
    # алгоритм Дейкстры
    while queue:
        cost, node, path = heapq.heappop(queue)
        if node in visited:
            continue
        if node == end:
            return path + [node], cost
        visited.add(node)
        for neighbor in graph[node]:
            heapq.heappush(queue, (cost + neighbor[1], neighbor[0], path + [node]))

    # если не удалось найти путь до конечной вершины
    return None, None


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=4567)
