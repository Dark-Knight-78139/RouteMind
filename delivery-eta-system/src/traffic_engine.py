import random

def simulate_traffic(G, congestion_level='normal'):
    """
    Modifies the dynamic_time attribute on edges to simulate traffic.
    congestion_level: 'low', 'normal', 'high', 'peak'
    """
    print(f"Simulating traffic for congestion level: {congestion_level}")
    
    multipliers = {
        'low': (0.8, 1.0),
        'normal': (1.0, 1.2),
        'high': (1.5, 2.5),
        'peak': (2.5, 4.0)
    }
    
    min_mult, max_mult = multipliers.get(congestion_level, (1.0, 1.0))
    
    for u, v, k, data in G.edges(keys=True, data=True):
        # Base travel time
        base_time = float(data.get('travel_time', data.get('length', 100) / 10.0))
        
        # Random congestion multiplier for this edge
        multiplier = random.uniform(min_mult, max_mult)
        
        # Simulate occasional road blockage (e.g., 0.5% chance during peak)
        if congestion_level == 'peak' and random.random() < 0.005:
            multiplier = 100.0 # Effectively blocked
            
        data['dynamic_time'] = base_time * multiplier
        data['traffic_multiplier'] = multiplier
        
    return G
