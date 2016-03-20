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
    colours = []

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
          colours.append('red')
        elif severity == 2:
          colours.append('green')
        elif severity == 3:
          colours.append('blue')

map_options = GMapOptions(lat=mean(lat), lng=mean(lon), map_type="roadmap", zoom=6)

plot = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="Car Accidents in the UK during 2014", webgl=True
)

source = ColumnDataSource(
    data=dict(
        lat = lat,
        lon = lon,
        cols = colours,
    )
)

cross = Cross(x="lon", y="lat", size=1, fill_alpha=0.8, line_color="cols")
plot.add_glyph(source, cross)

plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())

output_file("gmap_plot.html")
show(plot)
