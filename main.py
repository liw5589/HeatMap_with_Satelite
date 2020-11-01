import folium
from folium import plugins
import pandas as pd
import os

data = pd.read_csv("Long_Lat_Data.csv", encoding="UTF-8")
new_data = data[['CUSTOM.updateTime','OSD.latitude','OSD.longitude','OSD.altitude [m]']]

long_lat_list = []
final_list = []

for i in range(0,len(data)):
    string = str(data.iloc[i]['OSD.latitude']) + "," + str(data.iloc[i]['OSD.longitude'])
    long_lat_list.append(string)

for i in range(0,len(long_lat_list)-1):
    if(long_lat_list[i] != long_lat_list[i+1]):
        final_list.append(long_lat_list[i])

m = folium.Map( location=[new_data.iloc[0]['OSD.latitude'], new_data.iloc[0]['OSD.longitude']], zoom_start=17 ) 

long_list = []
lat_list = []
date_list = []

for i in range(0,len(new_data),20):
    long_list.append(new_data.iloc[i]['OSD.longitude'])
    lat_list.append(new_data.iloc[i]['OSD.latitude'])
    date_list.append(str(new_data.iloc[i]['CUSTOM.updateTime'])[3::])

print(date_list.index('12:16:36'))
print(date_list.index('12:21:46'))

lines = []

for i in range(0,116):
    A = { 'coordinates': [ 
            [long_list[i],lat_list[i]], 
            [long_list[i+1],lat_list[i+1]], ], 
            'dates': [ '2020-11-01T'+date_list[i], '2020-11-01T'+date_list[i+1] ], 'color': 'red' }
    lines.append(A)

for i in range(116,260):
    A = { 'coordinates': [ 
            [long_list[i],lat_list[i]], 
            [long_list[i+1],lat_list[i+1]], ], 
            'dates': [ '2020-11-01T'+date_list[i], '2020-11-01T'+date_list[i+1] ], 'color': 'blue' }
    lines.append(A)

for i in range(260,len(date_list)-1):
    A = { 'coordinates': [ 
            [long_list[i],lat_list[i]], 
            [long_list[i+1],lat_list[i+1]], ], 
            'dates': [ '2020-11-01T'+date_list[i], '2020-11-01T'+date_list[i+1] ], 'color': 'black' }
    lines.append(A)


# Lon, Lat order. 
# lines = [
#         { 'coordinates': [ 
#          [long_list[0],lat_list[0]], 
#          [long_list[1],lat_list[1]], ], 
#          'dates': [ '2017-06-02T'+date_list[0], '2017-06-02T'+date_list[1] ], 'color': 'red' },
#          { 'coordinates': [ 
#          [long_list[1],lat_list[1]], 
#          [long_list[2],lat_list[2]], ], 
#          'dates': [ '2017-06-02T'+date_list[1], '2017-06-02T'+date_list[2] ], 'color': 'red' }, 
#          { 'coordinates': [ 
#          [long_list[2],lat_list[2]], 
#          [long_list[3],lat_list[3]], ], 
#          'dates': [ '2017-06-02T'+date_list[2], '2017-06-02T'+date_list[3] ], 'color': 'red' }, 
#         ] 
                 
features = [ { 'type': 'Feature', 'geometry': { 'type': 'LineString', 'coordinates': 
                 line['coordinates'], }, 'properties': 
                 { 'times': line['dates'], 'style': 
                 { 'color': line['color'], 'weight': line['weight'] if 'weight' in line else 5 } } } 
                 for line in lines ] 
plugins.TimestampedGeoJson({ 'type': 'FeatureCollection', 'features': features, }, 
                 period='PT1M', add_last_point=False).add_to(m) 
m.save("TEST.html")
