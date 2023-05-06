import threading
from multiprocessing.pool import ThreadPool
from threading import Thread
from time import time
import numpy as np
import pandas as pd
from itertools import chain
from hoshenKopelman import HoshenKopelman
from matrix import Matrix
import multiprocessing as mp

N = 100


def full_statistics_for_N():
    full_stat = {}
    start_time = time()

    with mp.Pool(24) as p:
        answer = p.map(statistics_for_p, list(np.arange(5, 105, 5)))
        for i in range(1, 20):
            ind = round(i * 0.05, 2)
            full_stat[ind] = answer[i]

    # for i in range(1, 20):
    #     p = round(i * 0.05, 2)
    #     df = statistics_for_p(i*5)
    #     full_stat[p] = df

    df_full_stat = pd.DataFrame(full_stat)
    df_full_stat.to_excel(f'./percolation_{N}.xlsx')
    print('\nSequential execution time : %3.2f s.' % (time() - start_time))


def statistics_for_p(p):
    stat = {}
    for j in range(10000):
        print(N, ": ", p, ": ", j)
        stat[j] = count_clusters(p)
    return stat


def count_clusters(p):
    unique_numbers = np.unique(HoshenKopelman(Matrix(p, N).generation_matrix()).method())
    return len(unique_numbers)-1 if len(unique_numbers) > 1 else len(unique_numbers)


if __name__ == '__main__':
    full_statistics_for_N()

