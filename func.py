import copy
import sys

import numpy as np
import shapefile
import matplotlib.pyplot as plt
import time
from decimal import Decimal
import timeout_decorator


# function

# move start Point to intersection point

def move_point_to_intersection_point(x_start, y_start, start_point, end_point, size_of_each_coordinates):
    start_point[0] = start_point[0] - ((start_point[0] - x_start) % size_of_each_coordinates)
    start_point[1] = start_point[1] - ((start_point[1] - y_start) % size_of_each_coordinates)
    end_point[0] = end_point[0] - ((end_point[0] - x_start) % size_of_each_coordinates)
    end_point[1] = end_point[1] - ((end_point[1] - y_start) % size_of_each_coordinates)


# get distance from point to end point

def get_distance(point, end_point):
    x = abs(end_point[0] - point[0])
    y = abs(end_point[1] - point[1])
    d = np.sqrt(x ** Decimal(2) + y ** Decimal(2))
    return d


# check point is valid
def check_point_at_edge(next_point, x_start, x_end, y_start, y_end):
    if next_point[0] == x_start or next_point[0] == x_end or next_point[1] == y_start or next_point[1] == y_end:
        return True
    else:
        return False


# move point function
# return point(x, y, cost) or if invalid return False
def up(point, size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region):
    __point = copy.deepcopy(point)
    __point[1] += size_of_each_coordinates
    if check_point_at_edge(__point, x_start, x_end, y_start, y_end):
        return False

    cr_up_right = [((__point[0] - x_start) / size_of_each_coordinates),
                   ((__point[1] - y_start) / size_of_each_coordinates) - 1]
    cr_up_left = [((__point[0] - x_start) / size_of_each_coordinates) - 1,
                  ((__point[1] - y_start) / size_of_each_coordinates) - 1]
    cr_right = crime_region[int(cr_up_right[0])][int(cr_up_right[1])]
    cr_left = crime_region[int(cr_up_left[0])][int(cr_up_left[1])]
    if cr_right != 0 and cr_left != 0:
        return False
    elif cr_right != 0 or cr_left != 0:
        __point.append(Decimal('1.3'))
    else:
        __point.append(Decimal('1'))

    return __point


def right(point, size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region):
    __point = copy.deepcopy(point)
    __point[0] += size_of_each_coordinates
    if check_point_at_edge(__point, x_start, x_end, y_start, y_end):
        return False
    cr_up_right = [((__point[0] - x_start) / size_of_each_coordinates) - 1,
                   ((__point[1] - y_start) / size_of_each_coordinates)]
    cr_down_right = [((__point[0] - x_start) / size_of_each_coordinates) - 1,
                     ((__point[1] - y_start) / size_of_each_coordinates) - 1]
    cr_up = crime_region[int(cr_up_right[0])][int(cr_up_right[1])]
    cr_down = crime_region[int(cr_down_right[0])][int(cr_down_right[1])]
    if cr_up != 0 and cr_down != 0:
        return False
    elif cr_up != 0 or cr_down != 0:
        __point.append(Decimal('1.3'))
    else:
        __point.append(Decimal('1'))
    return __point


def down(point, size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region):
    __point = copy.deepcopy(point)
    __point[1] -= size_of_each_coordinates
    if check_point_at_edge(__point, x_start, x_end, y_start, y_end):
        return False
    cr_down_right = [((__point[0] - x_start) / size_of_each_coordinates),
                     ((__point[1] - y_start) / size_of_each_coordinates)]
    cr_down_left = [((__point[0] - x_start) / size_of_each_coordinates) - 1,
                    ((__point[1] - y_start) / size_of_each_coordinates)]
    cr_right = crime_region[int(cr_down_right[0])][int(cr_down_right[1])]
    cr_left = crime_region[int(cr_down_left[0])][int(cr_down_left[1])]

    if cr_right != 0 and cr_left != 0:
        return False
    elif cr_right != 0 or cr_left != 0:
        __point.append(Decimal('1.3'))
    else:
        __point.append(Decimal('1'))
    return __point


def left(point, size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region):
    __point = copy.deepcopy(point)
    __point[0] -= size_of_each_coordinates
    if check_point_at_edge(__point, x_start, x_end, y_start, y_end):
        return False
    cr_up_left = [((__point[0] - x_start) / size_of_each_coordinates),
                  ((__point[1] - y_start) / size_of_each_coordinates)]
    cr_down_left = [((__point[0] - x_start) / size_of_each_coordinates),
                    ((__point[1] - y_start) / size_of_each_coordinates) - 1]

    cr_up = crime_region[int(cr_up_left[0])][int(cr_up_left[1])]
    cr_down = crime_region[int(cr_down_left[0])][int(cr_down_left[1])]
    if cr_up != 0 and cr_down != 0:
        return False
    elif cr_up != 0 or cr_down != 0:
        __point.append(Decimal('1.3'))
    else:
        __point.append(Decimal('1'))
    return __point


def up_right(point, size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region):
    __point = copy.deepcopy(point)
    __point[0] += size_of_each_coordinates
    __point[1] += size_of_each_coordinates
    if check_point_at_edge(__point, x_start, x_end, y_start, y_end):
        return False
    cr_up_right = [((__point[0] - x_start) / size_of_each_coordinates) - 1,
                   ((__point[1] - y_start) / size_of_each_coordinates) - 1]
    cr_ur = crime_region[int(cr_up_right[0])][int(cr_up_right[1])]
    if cr_ur != 0:
        return False
    else:
        __point.append(Decimal('1.5'))
    return __point


def down_right(point, size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region):
    __point = copy.deepcopy(point)
    __point[0] += size_of_each_coordinates
    __point[1] -= size_of_each_coordinates
    if check_point_at_edge(__point, x_start, x_end, y_start, y_end):
        return False
    cr_down_right = [((__point[0] - x_start) / size_of_each_coordinates) - 1,
                     ((__point[1] - y_start) / size_of_each_coordinates)]
    cr_dr = crime_region[int(cr_down_right[0])][int(cr_down_right[1])]
    if cr_dr != 0:
        return False
    else:
        __point.append(Decimal('1.5'))
    return __point


def down_left(point, size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region):
    __point = copy.deepcopy(point)
    __point[0] -= size_of_each_coordinates
    __point[1] -= size_of_each_coordinates
    if check_point_at_edge(__point, x_start, x_end, y_start, y_end):
        return False
    cr_down_left = [((__point[0] - x_start) / size_of_each_coordinates),
                    ((__point[1] - y_start) / size_of_each_coordinates)]
    cr_dl = crime_region[int(cr_down_left[0])][int(cr_down_left[1])]
    if cr_dl != 0:
        return False
    else:
        __point.append(Decimal('1.5'))
    return __point


def up_left(point, size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region):
    __point = copy.deepcopy(point)
    __point[0] -= size_of_each_coordinates
    __point[1] += size_of_each_coordinates
    if check_point_at_edge(__point, x_start, x_end, y_start, y_end):
        return False
    cr_up_left = [((__point[0] - x_start) / size_of_each_coordinates),
                    ((__point[1] - y_start) / size_of_each_coordinates)-1]
    cr_ul = crime_region[int(cr_up_left[0])][int(cr_up_left[1])]
    if cr_ul != 0:
        return False
    else:
        __point.append(Decimal('1.5'))
    return __point


# find path
@timeout_decorator.timeout(10)
def find_path(x_start, x_end, y_start, y_end, start_point, end_point, size_of_each_coordinates, crime_region):
    # (x, y, distance to end point)
    path_coordinates = np.empty((0, 3), dtype=Decimal)

    if start_point == end_point:
        return path_coordinates


def main():
    start_time = time.time()
    x_start = Decimal('-73.59')
    x_end = Decimal('-73.55')
    y_start = Decimal('45.49')
    y_end = Decimal('45.53')

    start_point = [Decimal('-73.586'), Decimal('45.494')]
    end_point = [Decimal('-73.588'), Decimal('45.496')]
    crime_region = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=Decimal)
    size_of_each_coordinates = Decimal('0.002')
    # print(type(find_path(start_point, start_point, size_of_each_coordinates)))
    print(up_left(start_point, size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region))
    print("--- %s seconds ---" % (time.time() - start_time))


main()
