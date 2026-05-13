import osmnx as ox
import folium
import matplotlib.pyplot as plt

def plot_graph(G, show=True):
    """Plot the graph using OSMnx/Matplotlib."""
    fig, ax = ox.plot_graph(G, show=show, close=not show)
    return fig, ax

def get_route_map(G, route, congestion_level='normal'):
    """Create an interactive Folium map with the route."""
    # ox.plot_route_folium is deprecated in newer osmnx, using folium directly
    # Create the map base
    node1 = G.nodes[route[0]]
    m = folium.Map(location=[node1['y'], node1['x']], zoom_start=13)
    
    locations = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in route]
    folium.PolyLine(locations, color="blue", weight=5, opacity=0.8).add_to(m)
    
    folium.Marker(locations[0], popup="Start", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(locations[-1], popup="Destination", icon=folium.Icon(color='red')).add_to(m)
    
    return m
    
def get_comparison_map(G, route1, route2):
    """Plot two routes on the same Folium map for comparison."""
    # Map centered around the first node of route1
    node1 = G.nodes[route1[0]]
    m = folium.Map(location=[node1['y'], node1['x']], zoom_start=13)
    
    # Add route 1 (e.g. shortest)
    locations1 = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in route1]
    folium.PolyLine(locations1, color="blue", weight=5, opacity=0.8, tooltip="Shortest Route").add_to(m)
    
    # Add route 2 (e.g. fastest)
    locations2 = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in route2]
    folium.PolyLine(locations2, color="red", weight=5, opacity=0.8, tooltip="Dynamic/Fastest Route").add_to(m)
    
    # Add start and end markers
    folium.Marker(locations1[0], popup="Start", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(locations1[-1], popup="Destination", icon=folium.Icon(color='red')).add_to(m)
    
    return m

def plot_feature_importance(model, features):
    """Plot feature importance from the RandomForest model."""
    importances = model.feature_importances_
    plt.figure(figsize=(10, 6))
    plt.barh(features, importances)
    plt.xlabel('Importance')
    plt.title('Feature Importance for ETA Prediction')
    plt.tight_layout()
    return plt.gcf()
