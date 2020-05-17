import numpy as np
import matplotlib
import shapefile
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

shape = shapefile.Reader('Shape/crime_dt.shp', encoding='ISO-8859-1')
shapeRecords = shape.shapeRecords()
crimePoint = np.empty(shape=(0, 2), dtype=float)
# Get all crime location in crimePoint
for shapeR in shapeRecords:
    crimePoint = np.append(crimePoint, shapeR.shape.points, axis=0)
    # print(shapeR.shape.points)

print(crimePoint.ndim)
plt.subplot()
nr = np.random.random((2, 2))
print(nr)
plt.imshow(nr, cmap=plt.cm.BuPu_r)
plt.show()
