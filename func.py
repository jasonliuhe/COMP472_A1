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
    return Decimal(d)


# check point is valid
def check_point_at_edge(next_point, x_start, x_end, y_start, y_end):
    if next_point[0] == x_start or next_point[0] == x_end or next_point[1] == y_start or next_point[1] == y_end:
        return True
    else:
        return False


def removearray(L, arr):
    ind = 0
    size = len(L)
    while ind != size and not np.array_equal(L[ind], arr):
        ind += 1
    if ind != size:
        L.pop(ind)


# move point function
# return point(x, y, distance to end point + cost from start point ) or if invalid return False
def up(point, size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region, end_point):
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
    distance = get_distance((__point[0], __point[1]), end_point)
    if cr_right != 0 and cr_left != 0:
        return False
    elif cr_right != 0 or cr_left != 0:
        __point[2] = distance + Decimal('0.0013')
        # __point = np.append(__point, Decimal('1.3'))
    else:
        __point[2] = distance + Decimal('0.001')
        # __point = np.append(__point, Decimal('1'))

    return __point


def right(point, size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region, end_point):
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
    distance = get_distance((__point[0], __point[1]), end_point)
    if cr_up != 0 and cr_down != 0:
        return False
    elif cr_up != 0 or cr_down != 0:
        __point[2] = distance + Decimal('0.0013')
        # __point = np.append(__point, Decimal('1.3'))
    else:
        __point[2] = distance + Decimal('0.001')
        # __point = np.append(__point, Decimal('1'))
    return __point


def down(point, size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region, end_point):
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
    distance = get_distance((__point[0], __point[1]), end_point)
    if cr_right != 0 and cr_left != 0:
        return False
    elif cr_right != 0 or cr_left != 0:
        __point[2] = distance + Decimal('0.0013')
        # __point = np.append(__point, Decimal('1.3'))
    else:
        __point[2] = distance + Decimal('0.001')
        # __point = np.append(__point, Decimal('1'))
    return __point


def left(point, size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region, end_point):
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
    distance = get_distance((__point[0], __point[1]), end_point)
    if cr_up != 0 and cr_down != 0:
        return False
    elif cr_up != 0 or cr_down != 0:
        __point[2] = distance + Decimal('0.0013')
        # __point = np.append(__point, Decimal('1.3'))
    else:
        __point[2] = distance + Decimal('0.001')
        # __point = np.append(__point, Decimal('1'))
    return __point


def up_right(point, size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region, end_point):
    __point = copy.deepcopy(point)
    __point[0] += size_of_each_coordinates
    __point[1] += size_of_each_coordinates
    if check_point_at_edge(__point, x_start, x_end, y_start, y_end):
        return False
    cr_up_right = [((__point[0] - x_start) / size_of_each_coordinates) - 1,
                   ((__point[1] - y_start) / size_of_each_coordinates) - 1]
    cr_ur = crime_region[int(cr_up_right[0])][int(cr_up_right[1])]
    distance = get_distance((__point[0], __point[1]), end_point)
    if cr_ur != 0:
        return False
    else:
        __point[2] = distance + Decimal('0.0015')
        # __point = np.append(__point, Decimal('1.5'))
    return __point


def down_right(point, size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region, end_point):
    __point = copy.deepcopy(point)
    __point[0] += size_of_each_coordinates
    __point[1] -= size_of_each_coordinates
    if check_point_at_edge(__point, x_start, x_end, y_start, y_end):
        return False
    cr_down_right = [((__point[0] - x_start) / size_of_each_coordinates) - 1,
                     ((__point[1] - y_start) / size_of_each_coordinates)]
    cr_dr = crime_region[int(cr_down_right[0])][int(cr_down_right[1])]
    distance = get_distance((__point[0], __point[1]), end_point)
    if cr_dr != 0:
        return False
    else:
        __point[2] = distance + Decimal('0.0015')
        # __point = np.append(__point, Decimal('1.5'))
    return __point


def down_left(point, size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region, end_point):
    __point = copy.deepcopy(point)
    __point[0] -= size_of_each_coordinates
    __point[1] -= size_of_each_coordinates
    if check_point_at_edge(__point, x_start, x_end, y_start, y_end):
        return False
    cr_down_left = [((__point[0] - x_start) / size_of_each_coordinates),
                    ((__point[1] - y_start) / size_of_each_coordinates)]
    cr_dl = crime_region[int(cr_down_left[0])][int(cr_down_left[1])]
    distance = get_distance((__point[0], __point[1]), end_point)
    if cr_dl != 0:
        return False
    else:
        __point[2] = distance + Decimal('0.0015')
        # __point = np.append(__point, Decimal('1.5'))
    return __point


def up_left(point, size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region, end_point):
    __point = copy.deepcopy(point)
    __point[0] -= size_of_each_coordinates
    __point[1] += size_of_each_coordinates
    if check_point_at_edge(__point, x_start, x_end, y_start, y_end):
        return False
    cr_up_left = [((__point[0] - x_start) / size_of_each_coordinates),
                  ((__point[1] - y_start) / size_of_each_coordinates) - 1]
    cr_ul = crime_region[int(cr_up_left[0])][int(cr_up_left[1])]
    distance = get_distance((__point[0], __point[1]), end_point)
    if cr_ul != 0:
        return False
    else:
        __point[2] = distance + Decimal('0.0015')
        # __point = np.append(__point, Decimal('1.5'))
    return __point


# find path
@timeout_decorator.timeout(10)
def find_path(x_start, x_end, y_start, y_end, start_point, end_point, size_of_each_coordinates, crime_region):
    # (x, y, distance to end point)
    path_coordinates = np.array([start_point], dtype=Decimal)
    # Add cost to
    d_start_point = copy.deepcopy(start_point)
    d_start_point = np.append(d_start_point, Decimal(get_distance((d_start_point[0], d_start_point[1]), end_point)))
    # print('d_start_point', d_start_point)
    open_list = np.array([d_start_point], dtype=Decimal)
    close_list = np.empty((0, 3), dtype=Decimal)

    if start_point == end_point:
        return path_coordinates

    num = 0
    # start searching from open_list
    while open_list.size != 0:
        # Get all next point
        __up = up(open_list[0], size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region, end_point)
        __up_right = up_right(open_list[0], size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region,
                              end_point)
        __right = right(open_list[0], size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region, end_point)
        __down_right = down_right(open_list[0], size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region,
                                  end_point)
        __down = down(open_list[0], size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region, end_point)
        __down_left = down_left(open_list[0], size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region,
                                end_point)
        __left = left(open_list[0], size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region, end_point)
        __up_left = up_left(open_list[0], size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region,
                            end_point)

        # move start point to close_list from open_list
        close_list = np.append(close_list, [open_list[0]], axis=0)
        open_list = np.delete(open_list, 0, 0)

        # check all the points whether already in the open_list or close_list
        if type(__up) != bool:
            if __up[0] == end_point[0] and __up[1] == end_point[1]:
                print("find: ", __up[0], " ", __up[1], " ", __up[2])
                return path_coordinates
            point_exist = False
            for i in open_list:
                if i[0] == __up[0] and i[1] == __up[1]:
                    point_exist = True
                    break
            if not point_exist:
                for i in close_list:
                    if i[0] == __up[0] and i[1] == __up[1]:
                        point_exist = True
                        break
                if not point_exist:
                    open_list = np.append(open_list, [__up], axis=0)

        if type(__up_right) != bool:
            if __up_right[0] == end_point[0] and __up_right[1] == end_point[1]:
                print("find: ", __up_right[0], " ", __up_right[1], " ", __up_right[2])
                return path_coordinates
            point_exist = False
            for i in open_list:
                if i[0] == __up_right[0] and i[1] == __up_right[1]:
                    point_exist = True
                    break
            if not point_exist:
                for i in close_list:
                    if i[0] == __up_right[0] and i[1] == __up_right[1]:
                        point_exist = True
                        break
                if not point_exist:
                    open_list = np.append(open_list, [__up_right], axis=0)

        if type(__right) != bool:
            if __right[0] == end_point[0] and __right[1] == end_point[1]:
                print("find: ", __right[0], " ", __right[1], " ", __right[2])
                return path_coordinates
            point_exist = False
            for i in open_list:
                if i[0] == __right[0] and i[1] == __right[1]:
                    point_exist = True
                    break
            if not point_exist:
                for i in close_list:
                    if i[0] == __right[0] and i[1] == __right[1]:
                        point_exist = True
                        break
                if not point_exist:
                    open_list = np.append(open_list, [__right], axis=0)

        if type(__down_right) != bool:
            if __down_right[0] == end_point[0] and __down_right[1] == end_point[1]:
                print("find: ", __down_right[0], " ", __down_right[1], " ", __down_right[2])
                return path_coordinates
            point_exist = False
            for i in open_list:
                if i[0] == __down_right[0] and i[1] == __down_right[1]:
                    point_exist = True
                    break
            if not point_exist:
                for i in close_list:
                    if i[0] == __down_right[0] and i[1] == __down_right[1]:
                        point_exist = True
                        break
                if not point_exist:
                    open_list = np.append(open_list, [__down_right], axis=0)

        if type(__down) != bool:
            if __down[0] == end_point[0] and __down[1] == end_point[1]:
                print("find: ", __down[0], " ", __down[1], " ", __down[2])
                return path_coordinates
            point_exist = False
            for i in open_list:
                if i[0] == __down[0] and i[1] == __down[1]:
                    point_exist = True
                    break
            if not point_exist:
                for i in close_list:
                    if i[0] == __down[0] and i[1] == __down[1]:
                        point_exist = True
                        break
                if not point_exist:
                    open_list = np.append(open_list, [__down], axis=0)

        if type(__down_left) != bool:
            if __down_left[0] == end_point[0] and __down_left[1] == end_point[1]:
                print("find: ", __down_left[0], " ", __down_left[1], " ", __down_left[2])
                return path_coordinates
            point_exist = False
            for i in open_list:
                if i[0] == __down_left[0] and i[1] == __down_left[1]:
                    point_exist = True
                    break
            if not point_exist:
                for i in close_list:
                    if i[0] == __down_left[0] and i[1] == __down_left[1]:
                        point_exist = True
                        break
                if not point_exist:
                    open_list = np.append(open_list, [__down_left], axis=0)

        if type(__left) != bool:
            if __left[0] == end_point[0] and __left[1] == end_point[1]:
                print("find: ", __left[0], " ", __left[1], " ", __left[2])
                return path_coordinates
            point_exist = False
            for i in open_list:
                if i[0] == __left[0] and i[1] == __left[1]:
                    point_exist = True
                    break
            if not point_exist:
                for i in close_list:
                    if i[0] == __left[0] and i[1] == __left[1]:
                        point_exist = True
                        break
                if not point_exist:
                    open_list = np.append(open_list, [__left], axis=0)

        if type(__up_left) != bool:
            if __up_left[0] == end_point[0] and __up_left[1] == end_point[1]:
                print("find: ", __up_left[0], " ", __up_left[1], " ", __up_left[2])
                return path_coordinates
            point_exist = False
            for i in open_list:
                if i[0] == __up_left[0] and i[1] == __up_left[1]:
                    point_exist = True
                    break
            if not point_exist:
                for i in close_list:
                    if i[0] == __up_left[0] and i[1] == __up_left[1]:
                        point_exist = True
                        break
                if not point_exist:
                    open_list = np.append(open_list, [__up_left], axis=0)

        open_list = open_list[np.argsort(open_list[:, 2])]


# def main():
#     start_time = time.time()
#     x_start = Decimal('-73.59')
#     x_end = Decimal('-73.55')
#     y_start = Decimal('45.49')
#     y_end = Decimal('45.53')
#
#     start_point = [Decimal('-73.586'), Decimal('45.494')]
#     end_point = [Decimal('-73.588'), Decimal('45.496')]
#     crime_region = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#                             , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=Decimal)
#     size_of_each_coordinates = Decimal('0.002')
#     # print(up(start_point,size_of_each_coordinates, x_start, x_end, y_start, y_end, crime_region))
#     find_path(x_start, x_end, y_start, y_end, start_point, end_point, size_of_each_coordinates, crime_region)
#     print("--- %s seconds ---" % (time.time() - start_time))
#
#
# main()
