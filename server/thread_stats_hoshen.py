from threading import Thread
from time import time
import numpy as np
import pandas as pd
from hoshenKopelman import HoshenKopelman
from matrix import Matrix
import multiprocessing as mp

N = 150


def full_statistics_for_N():
    full_stat = {}

    for z in range(8, 10):
        start_time = time()
        with mp.Pool(24) as p:
            answer = np.array(p.map(statistics, list(np.arange(1000)))).T

            for i in range(len(answer)):
                ind = round((i+1) * 0.05, 2)
                full_stat[ind] = answer[i]

    # for i in range(1, 20):
    #     p = round(i * 0.05, 2)
    #     df = statistics_for_p(i*5)
    #     full_stat[p] = df

        df_full_stat = pd.DataFrame(full_stat)
        df_full_stat.to_excel(f'./percolation_{N}_{z}.xlsx')
        print('\nSequential execution time : %3.2f s.' % (time() - start_time))


def statistics(i):
    stat = {}
    for p in range(5, 100, 5):
        stat[p] = count_clusters(p)
    print("Success ", i)
    return list(stat.values())


def count_clusters(p):
    unique_numbers = np.unique(HoshenKopelman(Matrix(p, N).generation_matrix()).method())
    return len(unique_numbers)-1 if len(unique_numbers) > 1 else len(unique_numbers)


if __name__ == '__main__':
    full_statistics_for_N()

