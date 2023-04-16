import math
import random

import numpy as np


class Matrix:

    def __init__(self, concentration=80, size=50):
        self.concentration = concentration
        self.size = size

    def generation_matrix(self):
        return [[int(random.uniform(0, 1) <= self.concentration * 0.01) for _ in range(self.size)] for _ in
                range(self.size)]

    def cross_matrix(self):
        matrix = np.ones((self.size, self.size), dtype=int)
        matrix[0, 0], matrix[0, self.size - 1], matrix[self.size - 1, 0], matrix[
            self.size - 1, self.size - 1] = 0, 0, 0, 0
        for i in range(1, self.size - 1):
            for j in range(1, self.size - 1):
                if i == j or \
                        math.floor(self.size / 2) == i or \
                        math.floor(self.size / 2) == j or \
                        (math.floor((self.size - 1) / 2) - 1 != j and
                         math.floor((self.size - 1) / 2) - 1 != i) and \
                        (math.ceil(self.size / 2) != j and
                         math.ceil(self.size / 2) != i):
                    matrix[i, j] = 0
        return matrix.tolist()

    def vertical_zebra_matrix(self):
        return [[(1 if i % 2 == 0 else 0) for i in range(self.size)] for _ in range(self.size)]

    def horizontal_zebra_matrix(self):
        return [[(1 if j % 2 == 0 else 0) for _ in range(self.size)] for j in range(self.size)]

    def vertical_rain_matrix(self):
        return [[(random.randint(0, 1) if i % 2 == 0 else 0) for i in range(self.size)] for _ in range(self.size)]

    def horizontal_rain_matrix(self):
        return [[(random.randint(0, 1) if j % 2 == 0 else 0) for _ in range(self.size)] for j in range(self.size)]

    def chess_matrix(self):
        return [[((0 if j % 2 == 0 else 1) if i % 2 == 0 else (1 if j % 2 == 0 else 0)) for i in range(self.size)] for j
                in range(self.size)]

    def circles_matrix(self):
        matrix = np.zeros((self.size, self.size), dtype=int)
        for i in range((self.size + 1) // 2):
            matrix[i:self.size - i, i:self.size - i] = (1 if i % 2 == 0 else 0)
        return matrix.tolist()

    def H_matrix(self):
        block_size = 8
        matrix = np.zeros((self.size, self.size), dtype=int)
        for i in range(self.size//block_size):
            for j in range(self.size // block_size):
                matrix[2+j*block_size, i*block_size: i*block_size+5], \
                    matrix[i * block_size: i * block_size + 5, j * block_size], \
                    matrix[i * block_size: i * block_size + 5, j * block_size + 4] = 1, 1, 1
        return matrix


    def H_shift_matrix(self):
        block_size = 8
        matrix = np.zeros((self.size, self.size), dtype=int)
        for i in range(self.size//block_size):
            for j in range(self.size // block_size):
                matrix[2+j*block_size, i*block_size + block_size//2*j: i*block_size+5 + block_size//2*j], \
                    matrix[i * block_size: i * block_size + 5, j * block_size + i*block_size//2], \
                    matrix[i * block_size: i * block_size + 5, j * block_size + 4 + i*block_size//2] = 1, 1, 1
        return matrix


if __name__ == "__main__":
    print(np.array(Matrix(10, 20).vertical_rain_matrix()))
