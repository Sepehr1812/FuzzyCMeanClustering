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
    _sum = 0
    for i in range(len(a)):
        _sum += pow(a[i] - b[i], 2)

    return sqrt(_sum)


def fcm(data: list, v: list, m: int):
    u = [[0] * len(data)] * len(v)
    new_v = v

    while True:
        old_v = new_v
        # calculating u_ik
        for i in range(len(new_v)):
            for k in range(len(data)):
                denominator = 0

                x_k_minus_v_i = calculate_distance(data[k], new_v[i])
                for j in range(len(new_v)):
                    denominator += pow(x_k_minus_v_i / calculate_distance(data[k], new_v[j]), 2 / (m - 1))

                u[i][k] = 1 / denominator

        # calculating V_i
        new_v = []
        for i in range(len(v)):
            sum_elements = [0] * len(v[0])
            for k in range(len(data)):
                p = pow(u[i][k], m)
                for j in range(len(v[0])):
                    sum_elements[j] += p * data[k][j]

            den = 0
            for x in data[i]:
                den += pow(x, m)

            for j in range(len(sum_elements)):
                sum_elements[j] /= den

            new_v.append(tuple(sum_elements))

        # checking convergence
        print(new_v)


def main():
    m = 4  # m in u_ik formula

    data = read_data_set()  # data coordinates

    # trying different cluster numbers between 2 and 10
    for c in range(2, 3):
        v = initialize_v(c)
        fcm(data, v, m)


if __name__ == '__main__':
    main()
