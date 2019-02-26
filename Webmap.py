import folium
import pandas
# Import folium and pandas libraries.
# Folium will be used to define base map and custom layers
# Pandas will be used to extract data from txt files


data = pandas.read_csv("Volcanoes.txt")
# Save the txt file with csv method in the data variable
# In the text file there is a data frame about volcanos
lat = list(data["LAT"])
# Save the latitude from the dataframe as list into lat variable
lon = list(data["LON"])
# Save the longitude from the dataframe as list into long variable
elev = list(data ["ELEV"])
# Save the elevation from the dataframe as list into elev variable
name = list(data["NAME"])
# Save the volcanos names from the dataframe as list into name variable


def color_producer(elevation):
    # Define a function that evaluates the variable entered and returns
    # a string based on the value of the variable
    if elevation <= 1000:
        return "green"
    elif 1000<= elevation < 3000:
        return "orange"
    else:
        return "red"

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""
# HTML code to create the popup when clicking on the volcanos location
# defined in the marker layer


map = folium.Map(location=[70, -100], zoom_start=6, tiles="Mapbox Bright")
# Definition of map variable to store the base layer of the webmap

fgv = folium.FeatureGroup(name="Volcanos")
# Definition of the first feature group for the marker layer that locates
# the volcanos extracted from Volcanos.txt file

for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius = 6,
    popup=folium.Popup(iframe), fill_color=color_producer(el), color="grey",
    fill_opacity=0.7))
    # For loop plus zip function to define different features of the marker
    # layer. The 4 variable are iterated through the different colums that
    # are passed as arguments of zip funtion.
    #
    # In line 48 the iframe is defined for the popup message when clicking
    # in any of the markers that locates the volcanoself.
    #
    # In line 49 add_child method is applied to the feature group. The layer
    # is defined using CircleMarker method. The fill_color of the circle
    # marker is set thanks to color_producer function.

fgp = folium.FeatureGroup(name="Population")
# Definition of the second feature group for the polygon layer that displays
# the countries extracted from world.json txt file

fgp.add_child(folium.GeoJson(data=open("world.json", encoding="utf-8-sig").read(),
style_function=lambda x: {"fillColor":"green" if x["properties"]["POP2005"] <10000000
else "orange" if 10000000 <= x["properties"]["POP2005"] <= 100000000 else "red"}))
# Addchild method applied to the second feature group. The GeoJson method is
# used to define this polygon layer.
#
# The file world.json is open and saved in data variable using open () and
# read()
# The style_fuction uses a lambda function that gives a color to each country
# based on the population of that country

map.add_child(fgv)
# The first feature group is added to map variable using add_child method
map.add_child(fgp)
# The second feature group is added to map variable using add_child method
map.add_child(folium.LayerControl())
# Layer control added to the map to show or hide the two custom layers defined
# One is the marker layer (volcanos) and the other one is a polygon layer
# (population)

map.save("Map.html")
# Save the map with html extension
