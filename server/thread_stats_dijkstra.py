import random
from time import time
import numpy as np
import pandas as pd
import multiprocessing as mp
from dijkstra import Dijkstra

N = 50


def find_shotest(matrix):
    res = []
    minLength = 99999999999
    for i in range(len(matrix[0])):
        for j in range(len(matrix[0])):
            d = Dijkstra(matrix, (0, 1), (len(matrix) - 1, j))
            path, cost = d.method()
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
        for concentration in range(5, 100, 5):
            answer = np.array(p.map(statistics, list(np.column_stack((np.full(1000, concentration), np.arange(1000)))))).T
            full_stat['red'] = answer[0]
            full_stat['black'] = answer[1]
            df_full_stat = pd.DataFrame(full_stat)
            df_full_stat.to_excel(f'./percolation_{N}_con_{concentration}.xlsx')
            print('\nSequential execution time : %3.2f s.' % (time() - start_time))


def statistics(i):
    stat = {}
    red, black = count_cells(N, i[0])
    stat['red'] = red
    stat['black'] = black
    print("Success ", i[1])
    return list(stat.values())


if __name__ == '__main__':
    full_statistics_for_N()