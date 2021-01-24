""" clustering via FCM algorithm """

import re


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


def main():
    coordinates = read_data_set()  # data coordinates


if __name__ == '__main__':
    main()
