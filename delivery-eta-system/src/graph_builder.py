import osmnx as ox
import networkx as nx
import os
from src.utils import PROCESSED_DATA_DIR

def download_map(city_name):
    """
    Download the road network for a specific city using OSMnx.
    Returns a NetworkX MultiDiGraph.
    """
    print(f"Downloading map for {city_name}...")
    # Use network_type='drive' for delivery simulation
    G = ox.graph_from_place(city_name, network_type='drive')
    
    # Add edge speeds (km/h) based on highway type/attributes
    G = ox.add_edge_speeds(G)
    # Add travel times (seconds) based on edge lengths and speeds
    G = ox.add_edge_travel_times(G)
    
    # Add dynamic_time attribute initializing it to travel_time
    for u, v, k, data in G.edges(keys=True, data=True):
        if 'travel_time' in data:
            data['dynamic_time'] = data['travel_time']
        else:
            # Fallback if travel_time couldn't be calculated
            data['dynamic_time'] = data.get('length', 100) / 10.0 # roughly 36 km/h
            data['travel_time'] = data['dynamic_time']
            
        data['traffic_multiplier'] = 1.0
    
    return G

def save_graph(G, filename="city_graph.graphml"):
    """Saves the graph to the processed data directory."""
    path = os.path.join(PROCESSED_DATA_DIR, filename)
    ox.save_graphml(G, filepath=path)
    print(f"Graph saved to {path}")

def load_graph(filename="city_graph.graphml"):
    """Loads the graph from the processed data directory."""
    path = os.path.join(PROCESSED_DATA_DIR, filename)
    if os.path.exists(path):
        print(f"Loading graph from {path}...")
        return ox.load_graphml(filepath=path)
    else:
        raise FileNotFoundError(f"Graph file not found at {path}")

def get_nearest_node(G, lat, lon):
    """Find the nearest node in the graph to the given GPS coordinates."""
    return ox.distance.nearest_nodes(G, X=lon, Y=lat)
