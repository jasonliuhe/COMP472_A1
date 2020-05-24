import numpy as np
import shapefile
import matplotlib.pyplot as plt
import time
from decimal import Decimal
import timeout_decorator
import func


def main():

    # start timer
    start_time = time.time()

    # read shape file
    shape = shapefile.Reader('Shape/crime_dt.shp', encoding='ISO-8859-1')
    shapeRecords = shape.shapeRecords()

    # Get all crime location in crimePoint
    crimePoint = np.empty(shape=(0, 2), dtype=Decimal)
    for shapeR in shapeRecords:
        crimePoint = np.append(crimePoint, shapeR.shape.points, axis=0)


    # variables
    start_point = [Decimal('-73.562'), Decimal('45.49')]
    end_point = [Decimal('-73.557'), Decimal('45.526')]
    size_of_each_coordinates = Decimal('0.002')

    x_start = Decimal('-73.59')
    x_end = Decimal('-73.55')
    y_start = Decimal('45.49')
    y_end = Decimal('45.53')

    threshold_of_crime = Decimal('0.17')

    # GUI display maps
    # set x and y and grid
    fig, ax = plt.subplots(figsize=(20, 20))
    x_ticks = np.arange(x_start, x_end + Decimal('0.001'), size_of_each_coordinates)
    y_ticks = np.arange(y_start, y_end + Decimal('0.001'), size_of_each_coordinates)
    ax.set_xlim(x_start, x_end)
    ax.set_ylim(y_start, y_end)
    ax.set_xlabel('longitude')
    ax.set_ylabel('latitude')
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.grid(True, ls='--')

    # get region which over the threshold
    sizeofC = np.math.ceil((y_end - y_start) / size_of_each_coordinates)
    crime_region = np.zeros((sizeofC, sizeofC), int)
    for crime_loc in crimePoint:
        x = abs(np.math.ceil((x_start - Decimal(crime_loc[0])) / size_of_each_coordinates))
        y = sizeofC - (np.math.ceil((y_end - Decimal(crime_loc[1])) / size_of_each_coordinates))
        crime_region[x][y] += 1

    # print(crime_region)

    # get crimeNumberSorted
    crimeNumberSorted = np.sort(crime_region, axis=None)

    # get average
    avg = np.average(crime_region)
    print("average=", avg)

    # get standard deviation
    std = np.std(crimeNumberSorted)
    print("standard deviation", std)

    # get region after threshold
    thresholdOfNumOfCrime = Decimal(crimeNumberSorted.size) * threshold_of_crime
    # crime_region = np.where(crime_region > thresholdOfNumOfCrime, crime_region, 0)

    # set region
    for x in range(len(crime_region)):
        for y in range(len(crime_region[x])):
            ax.text(x_ticks[x] + size_of_each_coordinates / Decimal('2.5'),
                    y_ticks[y] + size_of_each_coordinates / Decimal('2.2'), crime_region[x][y])
            if crime_region[x][y] > thresholdOfNumOfCrime:
                ax.broken_barh([(x_ticks[x], size_of_each_coordinates)], (y_ticks[y], size_of_each_coordinates))
            else:
                crime_region[x][y] = 0

    # move point to intersection point
    func.move_point_to_intersection_point(x_start, y_start, start_point, end_point, size_of_each_coordinates)

    try:
        shortest_path = func.find_path(x_start, x_end, y_start, y_end, start_point, end_point, size_of_each_coordinates, crime_region)
        dp = end_point
        while len(shortest_path) != 0:
            if dp[0] == start_point[0] and dp[1] == start_point[1]:
                break
            for i in range(len(shortest_path)):
                if shortest_path[i][0] == dp[0] and shortest_path[i][1] == dp[1]:
                    plt.plot([dp[0], shortest_path[i][2]], [dp[1], shortest_path[i][3]], 'r--')
                    dp[0] = shortest_path[i][2]
                    dp[1] = shortest_path[i][3]
                    break


    except timeout_decorator.TimeoutError:
        print('Cannot find path.')
    plt.show()
    print("--- %s seconds ---" % (time.time() - start_time))


main()
