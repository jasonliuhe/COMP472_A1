import numpy as np
import shapefile
import matplotlib.pyplot as plt

shape = shapefile.Reader('Shape/crime_dt.shp', encoding='ISO-8859-1')
shapeRecords = shape.shapeRecords()
sizeOfCoordinates = 100
coordinatesRecords = np.zeros((sizeOfCoordinates,sizeOfCoordinates))
print(coordinatesRecords)
for i in range(len(shapeRecords)):
    x = shapeRecords[i].shape.__geo_interface__["coordinates"][0]
    y = shapeRecords[i].shape.__geo_interface__["coordinates"][1]

print(shapeRecords[0].shape.points)
for shapeR in shapeRecords:
    print(shapeR.record, " AT: ", shapeR.shape.points[0][0])


x = np.random.rand(1)
print(x)
y = np.random.rand(1)
print(y)
print(type(x))

plt.plot(x, y, 'o')

plt.grid(True, color='g', linestyle='-', linewidth=1)
plt.gca().patch.set_facecolor('0.9')

plt.show()
