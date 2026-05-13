import networkx as nx

def find_shortest_route(G, source, target):
    """Find the shortest distance route using Dijkstra."""
    return nx.shortest_path(G, source=source, target=target, weight='length')

def find_fastest_route(G, source, target):
    """Find the fastest route using Dijkstra (based on base travel time)."""
    return nx.shortest_path(G, source=source, target=target, weight='travel_time')

def find_dynamic_route(G, source, target, heuristic_func=None):
    """Find the route aware of dynamic traffic using A* or Dijkstra."""
    if heuristic_func is None:
        return nx.shortest_path(G, source=source, target=target, weight='dynamic_time')
    else:
        return nx.astar_path(G, source=source, target=target, heuristic=heuristic_func, weight='dynamic_time')

def get_route_stats(G, route):
    """Calculate the total distance, base time, and dynamic time for a given route."""
    distance = 0.0
    base_time = 0.0
    dynamic_time = 0.0
    
    for i in range(len(route) - 1):
        u = route[i]
        v = route[i+1]
        
        # Get the edge with the shortest dynamic_time if there are parallel edges
        edge_data = min(G.get_edge_data(u, v).values(), key=lambda x: x.get('dynamic_time', float('inf')))
        
        distance += float(edge_data.get('length', 0))
        base_time += float(edge_data.get('travel_time', 0))
        dynamic_time += float(edge_data.get('dynamic_time', 0))
        
    return {
        'distance_m': distance,
        'base_time_s': base_time,
        'dynamic_time_s': dynamic_time
    }
