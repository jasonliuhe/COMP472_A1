import copy
import numpy as np
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

def get_distance(point, end_point, size_of_each_coordinates):
    x = abs(end_point[0] - point[0]) / size_of_each_coordinates
    y = abs(end_point[1] - point[1]) / size_of_each_coordinates
    d = np.sqrt(x ** Decimal(2) + y ** Decimal(2))
    return Decimal(d)


# check point is valid
def check_point_at_edge(next_point, x_start, x_end, y_start, y_end):
    if next_point[0] == x_start or next_point[0] == x_end or next_point[1] == y_start or next_point[1] == y_end:
        return True
    else:
        return False


def remove_array(L, arr):
    ind = 0
    size = len(L)
    while ind != size and not np.array_equal(L[ind], arr):
        ind += 1
    if ind != size:
        L.pop(ind)


# shortest path of every checked point list (current_x, current_y, previous_x, previous_y, cost_from_start_point)
def check_shortest_path(__shortest_path, current_point, previous_point):
    new_cost = current_point[3]
    previous_point_distance = 0
    shortest_path = copy.deepcopy(__shortest_path)
    find_exist = False
    # find point in shortest_path list
    for i in range(len(shortest_path)):
        if shortest_path[i][0] == previous_point[0] and shortest_path[i][1] == previous_point[1]:
            previous_point_distance = shortest_path[i][4]
    for i in range(len(shortest_path)):
        if shortest_path[i][0] == current_point[0] and shortest_path[i][1] == current_point[1]:
            find_exist = True
            if (previous_point_distance + new_cost) < shortest_path[i][4]:
                # print("previous_point_distance", shortest_path[i][4])
                # print(previous_point_distance+new_cost)
                # print(shortest_path[i][0], " ", shortest_path[i][1], " ", shortest_path[i][2], " ", shortest_path[i][3], " ", shortest_path[i][4])
                # print("p0:", previous_point[0], " ", previous_point[1], " ", previous_point_distance + new_cost)
                shortest_path[i][2] = previous_point[0]
                shortest_path[i][3] = previous_point[1]
                shortest_path[i][4] = previous_point_distance + new_cost
                return shortest_path

    # not find point in shortest_path list
    if not find_exist:
        shortest_path = np.append(shortest_path, [
            [current_point[0], current_point[1], previous_point[0], previous_point[1],
             previous_point_distance + new_cost]], axis=0)
    return shortest_path


# move point function
# return point(x, y, distance to end point + cost from start point, new_cost) or if invalid return False
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
    distance = get_distance((__point[0], __point[1]), end_point, size_of_each_coordinates)
    if cr_right != 0 and cr_left != 0:
        return False
    elif cr_right != 0 or cr_left != 0:
        __point[2] = distance + Decimal('1.3') + point[2]
        __point = np.append(__point, Decimal('1.3'))
        # __point = np.append(__point, Decimal('1.3'))
    else:
        __point[2] = distance + Decimal('1') + point[2]
        __point = np.append(__point, Decimal('1'))
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
    distance = get_distance((__point[0], __point[1]), end_point, size_of_each_coordinates)
    if cr_up != 0 and cr_down != 0:
        return False
    elif cr_up != 0 or cr_down != 0:
        __point[2] = distance + Decimal('1.3') + point[2]
        __point = np.append(__point, Decimal('1.3'))
        # __point = np.append(__point, Decimal('1.3'))
    else:
        __point[2] = distance + Decimal('1') + point[2]
        __point = np.append(__point, Decimal('1'))
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
    distance = get_distance((__point[0], __point[1]), end_point, size_of_each_coordinates)
    if cr_right != 0 and cr_left != 0:
        return False
    elif cr_right != 0 or cr_left != 0:
        __point[2] = distance + Decimal('1.3') + point[2]
        __point = np.append(__point, Decimal('1.3'))
        # __point = np.append(__point, Decimal('1.3'))
    else:
        __point[2] = distance + Decimal('1') + point[2]
        __point = np.append(__point, Decimal('1'))
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
    distance = get_distance((__point[0], __point[1]), end_point, size_of_each_coordinates)
    if cr_up != 0 and cr_down != 0:
        return False
    elif cr_up != 0 or cr_down != 0:
        __point[2] = distance + Decimal('1.3') + point[2]
        __point = np.append(__point, Decimal('1.3'))
        # __point = np.append(__point, Decimal('1.3'))
    else:
        __point[2] = distance + Decimal('1') + point[2]
        __point = np.append(__point, Decimal('1'))
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
    distance = get_distance((__point[0], __point[1]), end_point, size_of_each_coordinates)
    if cr_ur != 0:
        return False
    else:
        __point[2] = distance + Decimal('1.5') + point[2]
        __point = np.append(__point, Decimal('1.5'))
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
    distance = get_distance((__point[0], __point[1]), end_point, size_of_each_coordinates)
    if cr_dr != 0:
        return False
    else:
        __point[2] = distance + Decimal('1.5') + point[2]
        __point = np.append(__point, Decimal('1.5'))
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
    distance = get_distance((__point[0], __point[1]), end_point, size_of_each_coordinates)
    if cr_dl != 0:
        return False
    else:
        __point[2] = distance + Decimal('1.5') + point[2]
        __point = np.append(__point, Decimal('1.5'))
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
    distance = get_distance((__point[0], __point[1]), end_point, size_of_each_coordinates)
    if cr_ul != 0:
        return False
    else:
        __point[2] = distance + Decimal('1.5') + point[2]
        __point = np.append(__point, Decimal('1.5'))
        # __point = np.append(__point, Decimal('1.5'))
    return __point


# find path
@timeout_decorator.timeout(10)
def find_path(x_start, x_end, y_start, y_end, start_point, end_point, size_of_each_coordinates, crime_region):
    # (x, y, distance to end point)
    path_coordinates = np.empty((0, 3), dtype=Decimal)
    # Add cost to
    d_start_point = copy.deepcopy(start_point)
    d_start_point = np.append(d_start_point, Decimal(
        get_distance((d_start_point[0], d_start_point[1]), end_point, size_of_each_coordinates)))
    # print('d_start_point', d_start_point)
    open_list = np.array([d_start_point], dtype=Decimal)
    close_list = np.empty((0, 3), dtype=Decimal)

    # shortest path of every checked point list (current_x, current_y, previous_x, previous_y, cost_from_start_point)
    shortest_path = np.empty((0, 5), dtype=Decimal)
    shortest_path = np.append(shortest_path,
                              [[start_point[0], start_point[1], start_point[0], start_point[1], Decimal(0)]], axis=0)

    if start_point == end_point:
        return path_coordinates

    num = 0
    # start searching from open_list
    while open_list.size != 0:
        num += 1
        # print(num)

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
        # path_coordinates = np.append(path_coordinates, [open_list[0]], axis=0)

        # check all the points whether already in the open_list or close_list
        if type(__up) != bool:
            # check the distance in shortest path list
            shortest_path = check_shortest_path(shortest_path, __up, open_list[0])

            if __up[0] == end_point[0] and __up[1] == end_point[1]:
                print("find: ", __up[0], " ", __up[1], " ", __up[2])
                return shortest_path
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
                    open_list = np.append(open_list, [[__up[0], __up[1], __up[2]]], axis=0)

        if type(__up_right) != bool:
            # check the distance in shortest path list
            shortest_path = check_shortest_path(shortest_path, __up_right, open_list[0])

            if __up_right[0] == end_point[0] and __up_right[1] == end_point[1]:
                print("find: ", __up_right[0], " ", __up_right[1], " ", __up_right[2])
                return shortest_path
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
                    open_list = np.append(open_list, [[__up_right[0], __up_right[1], __up_right[2]]], axis=0)

        if type(__right) != bool:
            # check the distance in shortest path list
            shortest_path = check_shortest_path(shortest_path, __right, open_list[0])
            if __right[0] == end_point[0] and __right[1] == end_point[1]:
                print("find: ", __right[0], " ", __right[1], " ", __right[2])
                return shortest_path
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
                    open_list = np.append(open_list, [[__right[0], __right[1], __right[2]]], axis=0)

        if type(__down_right) != bool:
            # check the distance in shortest path list
            shortest_path = check_shortest_path(shortest_path, __down_right, open_list[0])
            if __down_right[0] == end_point[0] and __down_right[1] == end_point[1]:
                print("find: ", __down_right[0], " ", __down_right[1], " ", __down_right[2])
                return shortest_path
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
                    open_list = np.append(open_list, [[__down_right[0], __down_right[1], __down_right[2]]], axis=0)

        if type(__down) != bool:
            # check the distance in shortest path list
            shortest_path = check_shortest_path(shortest_path, __down, open_list[0])
            if __down[0] == end_point[0] and __down[1] == end_point[1]:
                print("find: ", __down[0], " ", __down[1], " ", __down[2])
                return shortest_path
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
                    open_list = np.append(open_list, [[__down[0], __down[1], __down[2]]], axis=0)

        if type(__down_left) != bool:
            # check the distance in shortest path list
            shortest_path = check_shortest_path(shortest_path, __down_left, open_list[0])
            if __down_left[0] == end_point[0] and __down_left[1] == end_point[1]:
                print("find: ", __down_left[0], " ", __down_left[1], " ", __down_left[2])
                return shortest_path
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
                    open_list = np.append(open_list, [[__down_left[0], __down_left[1], __down_left[2]]], axis=0)

        if type(__left) != bool:
            # check the distance in shortest path list
            shortest_path = check_shortest_path(shortest_path, __left, open_list[0])
            if __left[0] == end_point[0] and __left[1] == end_point[1]:
                print("find: ", __left[0], " ", __left[1], " ", __left[2])
                return shortest_path
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
                    open_list = np.append(open_list, [[__left[0], __left[1], __left[2]]], axis=0)

        if type(__up_left) != bool:
            # check the distance in shortest path list
            shortest_path = check_shortest_path(shortest_path, __up_left, open_list[0])
            if __up_left[0] == end_point[0] and __up_left[1] == end_point[1]:
                print("find: ", __up_left[0], " ", __up_left[1], " ", __up_left[2])
                return shortest_path
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
                    open_list = np.append(open_list, [[__up_left[0], __up_left[1], __up_left[2]]], axis=0)

        open_list = np.delete(open_list, 0, 0)
        open_list = open_list[np.argsort(open_list[:, 2])]

    print("Cannot find path.")
    return path_coordinates


