from time import sleep

import numpy as np
from itertools import product

from flask_socketio import emit
from matrix import Matrix


class HoshenKopelman:

    def __init__(self, concentration=80, size=50):
        self.clustersVolume = {}
        self.concentration = concentration
        self.size = size

    def __create_cluster(self, count_clusters, i, j):
        count_clusters += 1
        self.clustersVolume[count_clusters] = [(i, j)]
        return count_clusters

    def __add_to_cluster(self, label, i, j):
        self.clustersVolume[label] += [(i, j)]
        return label

    def __clusters_merge(self, above, left, i, j):
        if above == left:
            return self.__add_to_cluster(above, i, j)
        self.clustersVolume[above] += self.clustersVolume[left] + [(i, j)]
        return above

    def __method(self, matrix):
        count_clusters = 2
        for i, j in product(range(len(matrix)), range(len(matrix[0]))):
            if matrix[i][j] == 0:
                continue
            empty_above = True if i == 0 else (matrix[i - 1][j] == 0)
            empty_left = True if j == 0 else (matrix[i][j - 1] == 0)

            # создаем новый кластер и ставим метку
            if empty_above and empty_left:
                count_clusters = self.__create_cluster(count_clusters, i, j)
                matrix[i][j] = count_clusters

            # добавляем клетку к кластеру
            elif empty_above ^ empty_left:
                matrix[i][j] = self.__add_to_cluster(matrix[i - 1][j] if not empty_above else matrix[i][j - 1], i, j)

            elif (not empty_above) and (not empty_left):
                above = matrix[i - 1][j]
                left = matrix[i][j - 1]
                matrix[i][j] = self.__clusters_merge(above, left, i, j)
                for x, y in self.clustersVolume[left]:
                    matrix[x][y] = matrix[i][j]

            # print(matrix)
            emit('hoshen_kopelman', {'matrix': matrix})

        return matrix

    def random_matrix(self):
        return self.__method(Matrix(self.concentration, self.size).generation_matrix())

    def cross_test(self):
        return self.__method(Matrix(self.concentration, self.size).cross_matrix())


if __name__ == "__main__":
    print(np.matrix(HoshenKopelman(80, 13).cross_test()))
