from time import sleep

import numpy as np
from itertools import product

from flask_socketio import emit
from matrix import Matrix


class HoshenKopelman:

    def __init__(self, matrix):
        self.clustersVolume = {}
        self.matrix = matrix

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

    def method(self):
        count_clusters = 2
        for i, j in product(range(len(self.matrix)), range(len(self.matrix[0]))):
            if self.matrix[i][j] == 0:
                continue
            empty_above = True if i == 0 else (self.matrix[i - 1][j] == 0)
            empty_left = True if j == 0 else (self.matrix[i][j - 1] == 0)

            # создаем новый кластер и ставим метку
            if empty_above and empty_left:
                count_clusters = self.__create_cluster(count_clusters, i, j)
                self.matrix[i][j] = count_clusters

            # добавляем клетку к кластеру
            elif empty_above ^ empty_left:
                self.matrix[i][j] = self.__add_to_cluster(self.matrix[i - 1][j] if not empty_above else self.matrix[i][j - 1], i, j)

            elif (not empty_above) and (not empty_left):
                above = self.matrix[i - 1][j]
                left = self.matrix[i][j - 1]
                self.matrix[i][j] = self.__clusters_merge(above, left, i, j)
                for x, y in self.clustersVolume[left]:
                    self.matrix[x][y] = self.matrix[i][j]

            # print(self.matrix)
            emit('hoshen_kopelman', {'matrix': self.matrix})

        return self.matrix


if __name__ == "__main__":
    print(np.matrix(HoshenKopelman(Matrix(80, 30).generation_matrix()).method()))
