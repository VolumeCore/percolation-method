import numpy as np
from itertools import product
import os
import random
from flask import Flask, render_template

project_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
client_dir = os.path.join(project_dir, 'client')
static_dir = os.path.join(client_dir, 'static')
template_dir = os.path.join(client_dir, 'templates')
app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/generateMatrix/<int:size>/<int:concentration>", methods=['GET'])
def genetation_matrix(concentration, size):
    return [[int(random.uniform(0, 1) <= concentration) for i in range(size)] for j in range(size)]


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4567)

    concentration = 0.45
    size = 10
    clustersVolume = {}

    clustersVolume.clear()
    A = genetation_matrix(concentration, size)
    HK = hoshenKopelman(A)
    print(np.matrix(HK))

    # тест на кресте (работает)
    #crossTest()

