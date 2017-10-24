import pyproj

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

for i in [topleft, topright, bottomleft, bottomright]:
    print('{}'.format(i))