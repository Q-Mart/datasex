import csv

from datetime import datetime

from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Cross, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
)

def mean(data):
  sum = 0
  for number in data:
    sum += number

  return sum/len(data)

fieldnames = ('Accident_Index','Location_Easting_OSGR','Location_Northing_OSGR',
              'Longitude','Latitude','Police_Force',
              'Accident_Severity','Number_of_Vehicles','Number_of_Casualties',
              'Date','Day_of_Week','Time,Local_Authority_(District)','Local_Authority_(Highway)',
              '1st_Road_Class','1st_Road_Number','Road_Type',
              'Speed_limit','Junction_Detail','Junction_Control',
              '2nd_Road_Class','2nd_Road_Number','Pedestrian_Crossing-Human_Control',
              'Pedestrian_Crossing-Physical_Facilities','Light_Conditions','Weather_Conditions',
              'Road_Surface_Conditions','Special_Conditions_at_Site','Carriageway_Hazards',
              'Urban_or_Rural_Area','Did_Police_Officer_Attend_Scene_of_Accident','LSOA_of_Accident_Location')

with open('DfTRoadSafety_Accidents_2014.csv','r') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames)

    index=[]
    lat=[]
    lon=[]
    no_vehicles=[]
    no_casualties=[]
    date=[]

    lat_and_long_by_severities=[[[],[]],[[],[]],[[],[]]]

    reader.next()

    for row in reader:
        index.append(row['Accident_Index'])
        lat.append(float(row['Latitude']))
        lon.append(float(row['Longitude']))
        no_vehicles.append(int(row['Number_of_Vehicles']))
        no_casualties.append(int(row['Number_of_Casualties']))
        date.append(datetime.strptime(row['Date'], '%d/%m/%Y'))

        severity = int(row['Accident_Severity']) 

        if severity == 1:
          lat_and_long_by_severities[0][0].append(float(row['Latitude']))
          lat_and_long_by_severities[0][1].append(float(row['Longitude']))
        elif severity == 2:
          lat_and_long_by_severities[1][0].append(float(row['Latitude']))
          lat_and_long_by_severities[1][1].append(float(row['Longitude']))
        elif severity == 3:
          lat_and_long_by_severities[2][0].append(float(row['Latitude']))
          lat_and_long_by_severities[2][1].append(float(row['Longitude']))

map_options = GMapOptions(lat=mean(lat), lng=mean(lon), map_type="roadmap", zoom=6)

plot = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="Car Accidents in the UK during 2014", webgl=True
)

source = ColumnDataSource(
    data=dict(
        lat = lat,
        lon = lon,
    )
)

fatal_source = ColumnDataSource(
    data=dict(
        fatal_lat=lat_and_long_by_severities[0][0],
        fatal_lon=lat_and_long_by_severities[0][1],
    )
)

severe_source = ColumnDataSource(
    data=dict(
        severe_lat=lat_and_long_by_severities[1][0],
        severe_lon=lat_and_long_by_severities[1][1],
    )
)

slight_source = ColumnDataSource(
    data=dict(
        slight_lat=lat_and_long_by_severities[2][0],
        slight_lon=lat_and_long_by_severities[2][1],
    )
)

fatal_cross = Cross(x="fatal_lon", y="fatal_lat", size=5, fill_alpha=0.8, line_color="red")
severe_cross = Cross(x="severe_lon", y="severe_lat", size=1, fill_alpha=0.8, line_color="green")
slight_cross = Cross(x="slight_lon", y="slight_lat", size=1, fill_alpha=0.8, line_color="blue")

plot.add_glyph(fatal_source, fatal_cross)
# plot.add_glyph(severe_source, severe_cross)
# plot.add_glyph(slight_source, slight_cross)

plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())

output_file("gmap_plot.html")
show(plot)
