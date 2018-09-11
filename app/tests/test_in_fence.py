import numpy
from shapely.geometry import Point as shapelyPoint
from shapely.geometry.polygon import Polygon


v0 = [7.115125222, -2.5]
v1 = [2, 3.5]
v2 = [-2, 4]
v3 = [-3, -3]
v4 = [0, -10]

np = numpy

lats_vect = np.array([v0[0], v1[0], v2[0], v3[0], v4[0]])
lons_vect = np.array([v0[1], v1[1], v2[1], v3[1], v4[1]])

x, y = 1.123654, 1

lats_longs_vect = np.column_stack((lats_vect, lons_vect))
polygon = Polygon(lats_longs_vect)
point = shapelyPoint(x, y)
_in = polygon.contains(point)

if _in:
    print('Entering the fence')
else:
    print('leaving from fence')



