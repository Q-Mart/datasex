import csv

from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
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

    lat=[]
    lon=[]

    reader.next()

    for row in reader:
        lat.append(float(row['Latitude']))
        lon.append(float(row['Longitude']))

map_options = GMapOptions(lat=mean(lat), lng=mean(lon), map_type="roadmap", zoom=6)

plot = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="Car Accidents in the UK during 2014"
)

source = ColumnDataSource(
    data=dict(
        lat = lat,
        lon = lon,
    )
)

circle = Circle(x="lon", y="lat", size=1, fill_color="blue", fill_alpha=0.8, line_color=None)
plot.add_glyph(source, circle)

plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
output_file("gmap_plot.html")
show(plot)
