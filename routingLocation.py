# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 00:42:26 2023

@author: HP
"""

from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
import geopy



def locationRouteFinder(locationCity, locationCountry):
    
    nominatim = Nominatim()

    areaId = nominatim.query(locationCity + ", " + locationCountry).areaId()
    
    nominatim_location = geopy.geocoders.Nominatim(user_agent="GetLoc")
    
    getLoc = nominatim_location.geocode(locationCity + " " + locationCountry)
    
    lati = getLoc.latitude
    longi = getLoc.longitude
    
    return (lati,longi)




def waterLocationFinderService(locationCity, locationCountry):
    
    nominatim = Nominatim()
    areaId = nominatim.query(locationCity + ", " + locationCountry).areaId()
    
    nominatim_location = geopy.geocoders.Nominatim(user_agent="GetLoc")
    
    getLoc = nominatim_location.geocode(locationCity + " " + locationCountry)
    
    
    overpass = Overpass()
    try:
        query = overpassQueryBuilder(area=areaId, elementType=['way', 'relation'], selector='"natural"="water"', includeGeometry=True)
        result = overpass.query(query)
        
        resTempStorage = result.elements()
        
        if(resTempStorage != []):
            firstElement = result.elements()[0]
            sdf = firstElement.geometry()['coordinates'][0]
            
        if(sdf!=[]):
            coordinatesPair = sdf[0]
            return coordinatesPair[::-1]
        
    except:
        return 'Data Not Found'
        
    

def routePairFunction(locationCity, locationCountry):
    # graph_area = (locationCity + ", " + locationCountry)
    
    
    # G = ox.graph_from_place(graph_area, network_type='drive')
    
    
    # G = ox.add_edge_speeds(G)
    # G = ox.add_edge_travel_times(G)
    
    
    # ox.save_graphml(G, "Manhattan.graphml")
    
    # fig, ax = ox.plot_graph(G, figsize=(10, 10), node_size=0, edge_color='y', edge_linewidth=0.2)
    
    origin_coordinates = locationRouteFinder(locationCity, locationCountry)
    destination_coordinates = waterLocationFinderService(locationCity, locationCountry)
    if(destination_coordinates!=0):
        urlApi = "https://map.project-osrm.org/?z=9&center=" + str(origin_coordinates[0]) + "%2C" + str(origin_coordinates[1]) + "&loc=" + str(origin_coordinates[0]) + "%2C" + str(origin_coordinates[1]) + "&loc=" + str(destination_coordinates[0]) + "%2C" + str(destination_coordinates[1]) + "&hl=en&alt=0&srv=1"
        return urlApi
    
def coordinateRouteFunction(originCoordinates, destinationCoordinates):
    print(originCoordinates, destinationCoordinates)
    if(destinationCoordinates != None):
        urlApi = "https://map.project-osrm.org/?z=9&center=" + str(originCoordinates[0]) + "%2C" + str(originCoordinates[1]) + "&loc=" + str(originCoordinates[0]) + "%2C" + str(originCoordinates[1]) + "&loc=" + str(destinationCoordinates[0]) + "%2C" + str(destinationCoordinates[1]) + "&hl=en&alt=0&srv=1"
        return urlApi
    else:
        return ''
    
    # origin_coordinates = (40.70195053163349, -74.01123198479581)
    # destination_coordinates = (40.87148739347057, -73.91517498611597)
    
    # origin_node = ox.nearest_nodes(G, origin_coordinates[1], origin_coordinates[0])
    # destination_node = ox.nearest_nodes(G, destination_coordinates[1], destination_coordinates[0])
    
    
    # shortest_route_by_distance = ox.shortest_path(G, origin_node, destination_node, weight='length')
    
    # fig, ax = ox.plot_graph_route(G, shortest_route_by_distance, route_color='y', route_linewidth=6, node_size=0)
    
    # shortest_route_by_travel_time = ox.shortest_path(G, origin_node, destination_node, weight='length')
    
    # fig, ax = ox.plot_graph_route(G, shortest_route_by_travel_time, route_color='y', route_linewidth=6, node_size=0)
    
    # fig, ax = ox.plot_graph_routes(G, routes=[shortest_route_by_distance, shortest_route_by_travel_time], route_colors=['r', 'y'], route_linewidth=6, node_size=0)
    
    # route = ox.distance.shortest_path(G, origin_node,destination_node)

    # updatedMapReference = ox.plot_route_folium(G, route, popup_attribute='length')
    
    # travel_time_in_seconds = nx.shortest_path_length(G, origin_node, destination_node, weight='travel_time')
    # travel_time_in_hours_minutes_seconds = str(timedelta(seconds=travel_time_in_seconds))
    # distance_in_meters = nx.shortest_path_length(G, origin_node, destination_node, weight='length')
    # distance_in_kilometers = distance_in_meters / 1000
    
    # htmlCode = "Info Box :<br>Travel time : "+str(travel_time_in_hours_minutes_seconds)+"<br>Distance in kilometers : "+str(distance_in_kilometers)
    
    # folium.Marker(location=[origin_coordinates[0], origin_coordinates[1]], popup=htmlCode, icon=folium.Icon(color='blue', icon='')).add_to(updatedMapReference)
    # folium.Marker(location=[destination_coordinates[0], destination_coordinates[1]], popup=htmlCode, icon=folium.Icon(color='red', icon='')).add_to(updatedMapReference)
    
    # updatedMapReference.save("templates/routeReference.html")
    
#routePairFunction("Jamshedpur", "India")