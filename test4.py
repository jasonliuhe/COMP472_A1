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
startPoint = [-73.587, 45.493]
endPoint = [-73.552, 45.492]
sizeOfEachCoordinates = 0.003
x_start = -73.59
x_end = -73.55
y_start = 45.49
y_end = 45.53

thresholdOfCrime = 0.25


# function

# move start Point to intersection point

def move_point_to_intersection_point(startpoint, endpoint, sizeofeachcoordinates):
    if int((startPoint[0] * 1000) % (sizeOfEachCoordinates * 1000)) != 0 :
        print((startPoint[0] * 1000) % (sizeOfEachCoordinates * 1000))
        print(11)
    if int((startPoint[1] * 1000) % (sizeOfEachCoordinates * 1000)) != 0 :
        print(int((startPoint[1] * 1000) % (sizeOfEachCoordinates * 1000)))
        print(22)
    if int((endPoint[0] * 1000) % (sizeOfEachCoordinates * 1000)) != 0 :
        print(int((endPoint[0] * 1000) % (sizeOfEachCoordinates * 1000)))
        print(33)
    if int((endPoint[1] * 1000) % (sizeOfEachCoordinates * 1000)) != 0 :
        print(int((endPoint[1] * 1000) % (sizeOfEachCoordinates * 1000)))
        print(44)
        # print(0-(np.math.ceil(abs(((endPoint[0]-(x_start-endPoint[0])%sizeOfEachCoordinates)*1000))))/1000)
        # startPoint[0] = float(0-(np.math.ceil(abs(((startPoint[0]-(x_start-startPoint[0])%sizeOfEachCoordinates)*1000))))/1000)
        # startPoint[1] = float(format(startPoint[1] - np.math.ceil(y_start-startPoint[1]) % sizeOfEachCoordinates, '.3f'))
        # endPoint[0] = float(0-(np.math.ceil(abs(((endPoint[0]-(x_start-endPoint[0])%sizeOfEachCoordinates)*1000))))/1000)
        # endPoint[1] = float(format(endPoint[1] - np.math.ceil(y_start-endPoint[1]) % sizeOfEachCoordinates, '.3f'))



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
