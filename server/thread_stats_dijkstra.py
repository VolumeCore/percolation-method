import random
from time import time
import numpy as np
import pandas as pd
from hoshenKopelman import HoshenKopelman
from matrix import Matrix
import multiprocessing as mp
from dijkstra import Dijkstra

N = 50
concentration = 60


def find_shotest(matrix):
    res = []
    minLength = 99999999999
    for i in range(len(matrix[0])):
        for j in range(len(matrix[0])):
            path, cost = Dijkstra(matrix, (0, 1), (len(matrix) - 1, j))
            if cost < minLength:
                res = path
                minLength = cost
    return res, minLength


def count_cells(size, concentration):
    count_black = 0
    count_red = 0
    matrix = [[int(random.randint(0, 100) <= concentration) for i in range(size)] for _ in
         range(size)]
    path, cost = find_shotest(matrix)
    for item in path:
        if matrix[item[0]][item[1]] == 1:
            count_black += 1
        else:
            count_red += 1
    return count_black, count_red


def full_statistics_for_N():
    full_stat = {}

    start_time = time()
    with mp.Pool(24) as p:
        answer = np.array(p.map(statistics, list(np.arange(10)))).T
        for i in range(len(answer)):
            ind = round((i + 1) * 0.05, 2)
            full_stat[ind] = answer[i]

    df_full_stat = pd.DataFrame(full_stat)
    df_full_stat.to_excel(f'./percolation_{N}_con_{concentration}.xlsx')
    print('\nSequential execution time : %3.2f s.' % (time() - start_time))


def statistics(i):
    stat = {}
    red, black = count_cells(N, concentration)
    stat['red'] = red
    stat['black'] = black
    print("Success ", i)
    return list(stat.values())


if __name__ == '__main__':
    full_statistics_for_N()