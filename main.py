""" clustering via FCM (Fuzzy-C-Mean) algorithm """

from math import pow, sqrt, log, e
from random import uniform
from re import split
from sys import float_info


def read_data_set():
    """
    read from a csv file as a data set and returns coordinates of data as an array of tuples
    """
    coordinates = []
    with open("data_set.csv", "r") as f:
        data = [split(",", line.rstrip('\n')) for line in f]

        for i in range(len(data)):
            data[i] = [float(x) for x in data[i]]

        for d in data:
            coordinates.append(tuple(d))

    return coordinates


def initialize_v(c: int, d: int):
    """
    initializes v array (array of the coordinates of cluster centers)
    :param c: number of clusters
    :param d: dimension of space
    :return: v array
    """
    v_arr = []

    for _ in range(c):
        v = []
        for j in range(d):
            v.append(uniform(0, 1))

        v_arr.append(tuple(v))

    return v_arr


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
        if calculate_distance(old_v[i], new_v[i]) > 0.001:  # 0.001 is a good number for checking convergence
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
        # print(new_v)
        if check_convergence(old_v, new_v):
            return new_v, u

    return new_v, u


def calculate_entropy(u: list[list[float]]):
    """
    :return: entropy of data based on clusters
    """
    s = 0
    for i in range(len(u)):
        for k in range(len(u[i])):
            s += u[i][k] * log(u[i][k], e)

    return -s / log(len(u), e)


def calculate_cost(data: list, u: list, v: list, m: int):
    """
    :return: cost of algorithm
    """
    s = 0
    for j in range(len(data)):
        for i in range(len(v)):
            s += pow(u[i][j], m) * pow(calculate_distance(data[j], v[i]), 2)

    return s


def main():
    t = 100  # termination condition; number of loops in FCM
    m = 5  # m in u_ik formula

    data = read_data_set()  # data coordinates

    # trying different cluster numbers between 2 and 10
    min_entropy = float_info.max
    min_index = 0
    v_arr = []
    u_arr = []
    for c in range(2, 11):
        v = initialize_v(c, len(data[0]))
        v, u = fcm(data, v, m, t)

        v_arr.append(v)
        u_arr.append(u)
        entropy = calculate_entropy(u)
        print(entropy)
        if entropy < min_entropy:
            min_entropy = entropy
            min_index = c - 2

    print("proper c:", min_index + 2)
    print("clusters centers:", v_arr[min_index])
    print("cost:", calculate_cost(data, u_arr[min_index], v_arr[min_index], m))


if __name__ == '__main__':
    main()
