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
    with mp.Pool(16) as p:
        answer = p.map(statistics_for_p, list(np.arange(0.05, 1.005, 0.05)))
        for i in range(1, 20):
            ind = round(i * 0.05, 2)
            full_stat[ind] = answer[i]

    # for i in range(1, 20):
    #     p = round(i * 0.05, 2)
    #     df = statistics_for_p(p)
    #     full_stat[p] = df

    df_full_stat = pd.DataFrame(full_stat)
    df_full_stat.to_excel(f'./percolation_{N}.xlsx')
    print('\nSequential execution time : %3.2f s.' % (time() - start_time))


def statistics_for_p(p):
    stat = {}
    for j in range(100):
        stat[j] = count_clusters(p)
    return stat


def count_clusters(p):
    flatten_HK = list(chain.from_iterable(HoshenKopelman(Matrix(p, N).generation_matrix()).method()))
    unique_numbers = list(set(flatten_HK))
    unique_numbers.pop(0)
    count_cl = len(unique_numbers)
    return count_cl


if __name__ == '__main__':
    full_statistics_for_N()
