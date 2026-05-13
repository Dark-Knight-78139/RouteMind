import os
import random
from src.utils import DEFAULT_CITY, MODELS_DIR
from src.graph_builder import download_map, save_graph, load_graph, get_nearest_node
from src.traffic_engine import simulate_traffic
from src.routing import find_shortest_route, find_fastest_route, find_dynamic_route, get_route_stats
from src.feature_engineering import generate_synthetic_data
from src.eta_model import ETAPredictor
from src.visualization import get_comparison_map

def run_simulation(city_name=DEFAULT_CITY, congestion_level='normal'):
    """Run a full delivery routing simulation."""
    print("=" * 50)
    print("Delivery ETA & Routing Simulation")
    print("=" * 50)
    
    # 1. Map Data
    try:
        G = load_graph()
    except FileNotFoundError:
        G = download_map(city_name)
        save_graph(G)
        
    # 2. Dynamic Traffic
    G = simulate_traffic(G, congestion_level=congestion_level)
    
    # 3. Model Training (if not already trained)
    predictor = ETAPredictor()
    model_path = os.path.join(MODELS_DIR, "eta_model.pkl")
    if not os.path.exists(model_path):
        data = generate_synthetic_data()
        data_path = os.path.join("data", "synthetic", "delivery_data.csv")
        predictor.train(data_path)
    else:
        predictor.load()
        
    # 4. Route Selection
    nodes = list(G.nodes())
    source_node = random.choice(nodes)
    target_node = random.choice(nodes)
    
    # Retry if same node or unreachable
    while source_node == target_node:
        target_node = random.choice(nodes)
        
    print(f"\nFinding routes from {source_node} to {target_node}...")
    
    try:
        shortest_route = find_shortest_route(G, source_node, target_node)
        dynamic_route = find_dynamic_route(G, source_node, target_node)
        
        shortest_stats = get_route_stats(G, shortest_route)
        dynamic_stats = get_route_stats(G, dynamic_route)
        
        print("\n--- Shortest Distance Route ---")
        print(f"Distance: {shortest_stats['distance_m']/1000:.2f} km")
        print(f"Expected Time (No Traffic): {shortest_stats['base_time_s']/60:.2f} mins")
        print(f"Expected Time (With Traffic): {shortest_stats['dynamic_time_s']/60:.2f} mins")
        
        print("\n--- Dynamic Congestion-Aware Route ---")
        print(f"Distance: {dynamic_stats['distance_m']/1000:.2f} km")
        print(f"Expected Time (No Traffic): {dynamic_stats['base_time_s']/60:.2f} mins")
        print(f"Expected Time (With Traffic): {dynamic_stats['dynamic_time_s']/60:.2f} mins")
        
        # 5. ETA Prediction
        # Gather features
        features = {
            'distance': dynamic_stats['distance_m'],
            'traffic_multiplier': 1.5 if congestion_level == 'high' else (2.5 if congestion_level == 'peak' else 1.0),
            'average_speed': 30.0,
            'hour_of_day': 14,
            'weather_condition': 0,
            'road_type': 2,
            'intersection_count': len(dynamic_route)
        }
        
        predicted_eta = predictor.predict(features)
        print(f"\nPredicted Delivery ETA (ML Model): {predicted_eta/60:.2f} mins")
        
        print("\nSimulation Complete.")
        
    except Exception as e:
        print(f"Error during routing: {e}")

if __name__ == "__main__":
    run_simulation()
