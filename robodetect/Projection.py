import pyproj
import numpy as np
from numbers import Number


# bounds of osm data
minlat =  40.7497
maxlat =  40.7687
minlon = -73.9916
maxlon = -73.9656

# construct a coordinate projection object for NYC-Manhatten
proj = pyproj.Proj(init='ESRI:102718')

# x, y-coordinates for the corners
topleft     = proj(minlon, maxlat)
topright    = proj(maxlon, maxlat)
bottomleft  = proj(minlon, minlat)
bottomright = proj(maxlon, minlat)

# because we cropped the viewbox to 250.78 x 250.78, we need to calculate the
# corner coordinates on the real map
width_viewbox  = 260.000000000105
height_viewbox = 250.77921174278

width_x_top    = abs(topleft[0]-topright[0])*height_viewbox/width_viewbox
width_x_bottom = abs(bottomleft[0]-bottomright[0])*height_viewbox/width_viewbox

topright    = (topleft[0] + width_x_top, topright[1])
bottomright = (bottomleft[0] + width_x_bottom, bottomright[1])

# those are the lat-lon bounds for our real map
maxlon_, minlat_ = proj(*bottomright, inverse=True)
minlon_, maxlat_ = proj(*topleft, inverse=True)

bounds_lat_lon = {
    'minlat': minlat_,
    'minlon': minlon_,
    'maxlat': maxlat_,
    'maxlon': maxlon_
}

bounds_pixel = {
    'xmin': 0,
    'xmax': 1000,
    'ymin': 0,
    'ymax': 1000
}


class Projector(object):
    def __init__(self,
                 bounds_lat_lon: dict,
                 bounds_pixel: dict,
                 proj: pyproj.Proj=pyproj.Proj(init='ESRI:102718')):
        self.bounds_lat_lon = bounds_lat_lon
        self.bounds_pixel = bounds_pixel
        self.proj = proj

        topleft = proj(bounds_lat_lon['minlon'], bounds_lat_lon['maxlat'])
        bottomright = proj(bounds_lat_lon['maxlon'], bounds_lat_lon['minlat'])

        xmin = topleft[0]
        xmax = bottomright[0]
        ymin = bottomright[1]
        ymax = topleft[1]

        self.scale_x = (xmax-xmin)/bounds_pixel['xmax']
        self.scale_y = (ymin-ymax)/bounds_pixel['ymax']
        self.trans_x = xmin
        self.trans_y = ymin


    def pixel_coordinate_to_lon_lat(self, x: Number, y: Number):
        x_ = self.scale_x * x + self.trans_x
        y_ = self.scale_y * y + self.trans_y

        return self.proj(x_, y_, inverse=True)


    def distance(self, point1: dict, point2: dict):
        p1_cart = np.array([self.proj(point1['lon'], point1['lat'])])
        p2_cart = np.array([self.proj(point2['lon'], point2['lat'])])
        return np.linalg.norm(p1_cart-p2_cart)


hackathon_projector = Projector(bounds_lat_lon, bounds_pixel)

if __name__ == '__main__':
    for x_y in [topleft, topright, bottomleft, bottomright]:
        print(x_y)

    for coordinate in [minlat_, maxlat_, minlon_, maxlon_]:
        print(coordinate)


    # test lat-lon-calculation
    for x, y in [[0,0], [1000,0], [1000,1000], [0,1000]]:
        print(hackathon_projector.pixel_coordinate_to_lon_lat(x, y))

