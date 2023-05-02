import numpy as np
from itertools import product
import os
import random
from flask import Flask, render_template, request, json
import heapq

project_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
client_dir = os.path.join(project_dir, 'client')
static_dir = os.path.join(client_dir, 'static')
template_dir = os.path.join(client_dir, 'templates')
app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)


@app.route("/")
def hello():
    return render_template('index.html')


@app.route("/generateMatrix/<int:size>/<int:concentration>", methods=['GET'])
def generation_matrix(concentration, size):
    return [[int(random.uniform(0, 1) <= concentration * 0.01) for i in range(size)] for j in range(size)]

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

def createCluster(countClusters, i, j):
    global clustersVolume
    countClusters += 1
    clustersVolume[countClusters] = [(i, j)]
    return countClusters


def addToCluster(label, i, j):
    print(f'addToCluster label {label}')
    clustersVolume[label] += [(i, j)]
    return label


def clustersMerge(above, left, i, j):
    global clustersVolume
    if above == left:
        return addToCluster(above, i, j)
    clustersVolume[above] += clustersVolume[left] + [(i, j)]
    return above


def hoshenKopelman(A):
    countClusters = 2
    for i, j in product(range(len(A)), range(len(A[0]))):
        if A[i][j] == 0:
            continue
        emptyAbove = True if i == 0 else (A[i - 1][j] == 0)
        emptyLeft = True if j == 0 else (A[i][j - 1] == 0)

        # создаем новый кластер и ставим метку
        if emptyAbove and emptyLeft:
            countClusters = createCluster(countClusters, i, j)
            A[i][j] = countClusters

        # добавляем клетку к кластеру
        elif emptyAbove ^ emptyLeft:
            A[i][j] = addToCluster(A[i - 1][j] if not emptyAbove else A[i][j - 1], i, j)

        elif (not emptyAbove) and (not emptyLeft):
            above = A[i - 1][j]
            left = A[i][j - 1]
            A[i][j] = clustersMerge(above, left, i, j)
            for x, y in clustersVolume[left]:
                A[x][y] = A[i][j]

        # print(f'Iteration {i, j}')
        print(np.matrix(A))
        print(clustersVolume)
    return A


def crossTest():
    A = np.zeros((7, 7), dtype=int)
    A[0, 1] = 1
    A[0, 2] = 1
    A[0, 3] = 1
    A[0, 4] = 1
    A[0, 5] = 1
    A[1, 0] = 1
    A[1, 2] = 1
    A[1, 4] = 1
    A[1, 6] = 1
    A[2, 0] = 1
    A[2, 1] = 1
    A[2, 4] = 1
    A[2, 5] = 1
    A[2, 6] = 1
    A[3, 0] = 1
    A[3, 6] = 1
    A[4, 0] = 1
    A[4, 1] = 1
    A[4, 2] = 1
    A[4, 5] = 1
    A[4, 6] = 1
    A[5, 0] = 1
    A[5, 2] = 1
    A[5, 4] = 1
    A[5, 6] = 1
    A[6, 1] = 1
    A[6, 2] = 1
    A[6, 3] = 1
    A[6, 4] = 1
    A[6, 5] = 1
    HK = hoshenKopelman(A)
    print(np.matrix(HK))


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
    app.run(host='0.0.0.0', port=4567)

    # concentration = 45
    # size = 10
    # clustersVolume = {}

    # clustersVolume.clear()
    # A = generation_matrix(concentration, size)
    # HK = hoshenKopelman(A)
    # print(np.matrix(HK))

    # тест на кресте (работает)
    # crossTest()
