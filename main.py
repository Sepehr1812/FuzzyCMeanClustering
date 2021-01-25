""" clustering via FCM (Fuzzy-C-Mean) algorithm """

import re
from math import pow, sqrt
from random import uniform


def read_data_set():
    """
    read from a csv file as a data set and returns coordinates of data as an array of tuples
    """
    coordinates = []
    with open("data_set.csv", "r") as f:
        data = [re.split(",", line.rstrip('\n')) for line in f]
        for d in data:
            coordinates.append((round(float(d[0]), 9), round(float(d[1]), 9)))

    return coordinates


def initialize_v(c: int):
    """
    initializes v array (array of the coordinates of cluster centers)
    :param c: number of clusters
    :return: v array
    """
    v = []

    for i in range(c):
        v.append((uniform(0, 1), uniform(0, 1)))

    return v


def calculate_distance(a, b):
    """
    :return: distance of a and b in their vector space
    """
    _sum = 0
    for i in range(len(a)):
        _sum += pow(a[i] - b[i], 2)

    return sqrt(_sum)


def check_convergence(old_v: list, new_v: list):
    """
    :return: True if we reach convergence, False otherwise
    """
    for i in range(len(old_v)):
        if calculate_distance(old_v[i], new_v[i]) > 0.001:
            return False
    return True


def fcm(data: list, v: list, m: int, t: int):
    """
    performing FCM algorithm
    :param data: all data coordinates
    :param v: initial cluster centers array
    :param m: param m that is used in formulas
    :param t: number of loops (termination condition)
    :return: array of cluster centers and u_ik if it reached to a convergence
    """
    u = [[0 for _ in range(len(data))] for _ in range(len(v))]
    new_v = v

    for _ in range(t):
        old_v = new_v

        # calculating u_ik
        for i in range(len(v)):
            for k in range(len(data)):
                denominator = 0

                x_k_minus_v_i = calculate_distance(data[k], new_v[i])
                for j in range(len(v)):
                    denominator += pow(x_k_minus_v_i / calculate_distance(data[k], new_v[j]), 2 / (m - 1))

                u[i][k] = 1 / denominator

        # calculating V_i
        new_v = []
        for i in range(len(v)):
            sum_elements = [0] * len(v[0])  # tuple of the numerator
            for k in range(len(data)):
                p = pow(u[i][k], m)
                for j in range(len(v[0])):
                    sum_elements[j] += p * data[k][j]

            den = 0
            for _u in u[i]:
                den += pow(_u, m)

            for j in range(len(sum_elements)):
                sum_elements[j] /= den

            new_v.append(tuple(sum_elements))

        # checking convergence
        print(new_v)
        if check_convergence(old_v, new_v):
            return new_v, u

    return new_v, u


def main():
    t = 100  # termination condition; number of loops in FCM
    m = 3  # m in u_ik formula

    data = read_data_set()  # data coordinates

    # trying different cluster numbers between 2 and 10
    for c in range(5, 6):
        v = initialize_v(c)
        fcm(data, v, m, t)


if __name__ == '__main__':
    main()
