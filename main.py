""" clustering via FCM algorithm """

import re
from random import uniform


def read_data_set():
    """
    read from a csv file as a data set and returns coordinates of data as an array of tuples
    """
    coordinates = []
    with open("data_set.csv", "r") as f:
        data = [re.split(",", line.rstrip('\n')) for line in f]
        for d in data:
            coordinates.append((float(d[0]), float(d[1])))

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


def main():
    coordinates = read_data_set()  # data coordinates

    # trying different cluster numbers between 2 and 10
    for c in range(2, 11):
        v = initialize_v(c)


if __name__ == '__main__':
    main()
