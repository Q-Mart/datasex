import csv

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

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


    source = ColumnDataSource()
    source.add(lon)
    source.add(lat)
    p = figure()
    p.circle(x=lon, y=lat, alpha=0.9, source=source)
    output_file("geojson.html")
    show(p)
