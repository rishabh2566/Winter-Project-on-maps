import pandas as pd
import geopandas as gpd
import folium
import os
import json
from folium.plugins import HeatMap, MarkerCluster
from folium import Choropleth, Circle, Marker

def embed_map(m, file_name):
    from IPython.display import IFrame
    m.save(file_name)
    return IFrame(file_name, width='100%', height='500px')

# Create map object
m = folium.Map(location=[23.2599, 77.4126],
 zoom_start=5 ,  
 min_zoom=5 , 
 max_zoom=9, 
 opacity=0.8,
 tiles='Stamen Terrain' ,
 #prefer_canvas=True,
 # Uncomment. may improve performance for vector layers
 zoom_control=True)

folium.TileLayer('openstreetmap',
	 zoom_start=5 ,  
	 min_zoom=5 , 
	 max_zoom=9, 
	 opacity=0.8,).add_to(m)
folium.TileLayer('cartodbpositron',
	 zoom_start=5 ,  
	 min_zoom=5 , 
	 max_zoom=9, 
	 opacity=0.8,).add_to(m)
folium.TileLayer('cartodbpositronnolabels',
	 zoom_start=5 ,  
	 min_zoom=5 , 
	 max_zoom=9, 
	 opacity=0.8,).add_to(m)
folium.TileLayer('stamentonerbackground',
	 zoom_start=5 ,  
	 min_zoom=5 , 
	 max_zoom=9, 
	 opacity=0.8,).add_to(m)

m.fit_bounds([[2.0469, 45.3182], [38.4872, 106.2309]])

#reading data   and		plotting markers
data = pd.read_csv('1_4964_pt_details_witht_str.txt', sep="\t", header=None, names=["id", "lat", "long", "Value"])

tooltip="Insert Name. Click to open."
mc = MarkerCluster()

for i in range(1,4965):
	fx=str(int(data['Value'][i])+2)
	mc.add_child( Marker([float(data['lat'][i]),float(data['long'][i])] , tooltip=tooltip,
		popup="<b>Value  : </b>"+data['Value'][i]+ "<br> <b>fx=value+2 : </b>"+fx ))

m.add_child(mc)


# reading GEOJSON

dist_geo = os.path.join('india_district.geojson')

folium.Choropleth(
	geo_data=dist_geo, name='District',
	key_on=str('feature.properties.ID_1') , 
	fill_color='grey',
	fill_opacity=0.5,
	line_color='black',
 	line_opacity=0.3,
	legend_name='Random IndeX',
	highlight=True,
	show=False,
	).add_to(m)



riskdata = pd.read_csv('random.csv')


states_geo = os.path.join('india_state.geojson')

folium.Choropleth(
	geo_data=states_geo, name='States',
	data=riskdata,
	key_on=str('feature.properties.ID_1') , 
	columns=['ID', 'Index'],
	fill_color='YlGn' ,
	fill_opacity=0.7,
 	line_opacity=0.2,
	legend_name='Random IndeX',
	smooth_factor=2.5,
	highlight=True,
	).add_to(m)


folium.LayerControl(position='topright', collapsed=True, autoZIndex=True).add_to(m)
# Display the map
m.save('mapmarker.html')
