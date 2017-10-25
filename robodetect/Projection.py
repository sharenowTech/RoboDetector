import pyproj
from numbers import Number


minlat =  40.7497
maxlat =  40.7687
minlon = -73.9916
maxlon = -73.9656

# construct a coordinate projection object for NYC-Manhatten
proj = pyproj.Proj(init='ESRI:102718')

topleft     = proj(minlon, maxlat)
topright    = proj(maxlon, maxlat)
bottomleft  = proj(minlon, minlat)
bottomright = proj(maxlon, minlat)

# because we cropped the viewbox to 250.78 x 250.78, we need to calculate the
# real corner coordinates on the map
width_viewbox  = 260.000000000105
height_viewbox = 250.77921174278

width_x_top    = abs(topleft[0]-topright[0]) * height_viewbox/width_viewbox
width_x_bottom = abs(bottomleft[0]-bottomright[0]) * height_viewbox/width_viewbox

topright    = (topleft[0] + width_x_top, topright[1])
bottomright = (bottomleft[0] + width_x_bottom, bottomright[1])

maxlon_, minlat_ = proj(*bottomright, inverse=True)
minlon_, maxlat_ = proj(*topleft, inverse=True)


def pixel_coordinate_to_lat_lon(x: Number, y: Number):
    # first off all, our pixel coordinates are flipped in y orientation
    # y-coordinates at the bottom are bigger than at the top
    pass


if __name__ == '__main__':
    for x_y in [topleft, topright, bottomleft, bottomright]:
        print(x_y)

    for coordinate in [minlat_, maxlat_, minlon_, maxlon_]:
        print(coordinate)

