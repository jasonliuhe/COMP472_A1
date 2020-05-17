import numpy as np
import shapefile
import matplotlib.pyplot as plt
import time

start_time = time.time()
shape = shapefile.Reader('Shape/crime_dt.shp', encoding='ISO-8859-1')
shapeRecords = shape.shapeRecords()

crimePoint = np.empty(shape=(0, 2), dtype=float)
# Get all crime location in crimePoint
for shapeR in shapeRecords:
    crimePoint = np.append(crimePoint, shapeR.shape.points, axis=0)
    # print(shapeR.shape.points)

# GUI
# variable
startPoint = [-73.585, 45.495]
endPoint = [-73.553, 45.492]
sizeOfEachCoordinates = 0.002

x_start = -73.59
x_end = -73.55
y_start = 45.49
y_end = 45.53

thresholdOfCrime = 0.40


# function

# move start Point to intersection point

def move_point_to_intersection_point(startpoint, endpoint, sizeofeachcoordinates):
    # startPoint[0] = startPoint[0] - ((startPoint[0] - x_start) % sizeOfEachCoordinates)
    # startPoint[1] = startPoint[1] - ((startPoint[1] - y_start) % sizeOfEachCoordinates)
    # endPoint[0] = endPoint[0] - ((endPoint[0] - x_start) % sizeOfEachCoordinates)
    # endPoint[1] = endPoint[1] - ((endPoint[1] - y_start) % sizeOfEachCoordinates)
    print((4549.2 - 4549))

    print(startPoint[0])
    print(startPoint[1])
    print(endPoint[0])
    print(endPoint[1])



# set x and y and grid
fig, ax = plt.subplots(figsize=(20, 20))
x_ticks = np.arange(x_start, x_end, sizeOfEachCoordinates)
y_ticks = np.arange(y_start, y_end + 0.001, sizeOfEachCoordinates)
ax.set_xlim(x_start, x_end)
ax.set_ylim(y_start, y_end)
ax.set_xlabel('longitude')
ax.set_ylabel('latitude')
ax.set_xticks(x_ticks)
ax.set_yticks(y_ticks)
ax.grid(True, ls='--')

# get region which over the threshold
sizeofC = np.math.ceil((y_end - y_start) / sizeOfEachCoordinates)
crimeRegion = np.zeros((sizeofC, sizeofC), int)
for crimeloc in crimePoint:
    x = abs(np.math.ceil((x_start - crimeloc[0]) / sizeOfEachCoordinates))
    y = sizeofC - (np.math.ceil((y_end - crimeloc[1]) / sizeOfEachCoordinates))
    crimeRegion[x][y] += 1

# get region after threshold
thresholdOfNumOfCrime = np.math.ceil(crimeRegion.max() * thresholdOfCrime)
crimeRegion = np.where(crimeRegion > thresholdOfNumOfCrime, crimeRegion, 0)

# set region
for x in range(len(crimeRegion)):
    for y in range(len(crimeRegion[x])):
        if crimeRegion[x][y] > 0:
            ax.broken_barh([(x_ticks[x], sizeOfEachCoordinates)], (y_ticks[y], sizeOfEachCoordinates))

# draw line
path_x = []
path_y = []

move_point_to_intersection_point(startPoint, endPoint, sizeOfEachCoordinates)
print(startPoint)
print(endPoint)
# plt.plot(path_x, path_y, 'r--')
plt.plot([startPoint[0], endPoint[0]], [startPoint[1], endPoint[1]], 'r--')

plt.show()
print("--- %s seconds ---" % (time.time() - start_time))
