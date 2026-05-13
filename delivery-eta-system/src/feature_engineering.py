import pandas as pd
import numpy as np
import random
import os
from src.utils import SYNTHETIC_DATA_DIR

def generate_synthetic_data(num_samples=5000):
    """Generates synthetic delivery data for training the ETA prediction model."""
    print(f"Generating {num_samples} synthetic delivery records...")
    
    data = []
    for _ in range(num_samples):
        distance = random.uniform(500, 15000) # 500m to 15km
        hour_of_day = random.randint(0, 23)
        
        # Traffic multiplier depends on hour of day
        if 8 <= hour_of_day <= 10 or 17 <= hour_of_day <= 20: # Peak hours
            traffic_multiplier = random.uniform(2.0, 4.0)
        elif 0 <= hour_of_day <= 5: # Night
            traffic_multiplier = random.uniform(0.8, 1.0)
        else: # Normal
            traffic_multiplier = random.uniform(1.0, 2.0)
            
        weather_condition = random.choice([0, 1, 2]) # 0: Clear, 1: Rain, 2: Storm
        if weather_condition == 1:
            traffic_multiplier *= 1.2
        elif weather_condition == 2:
            traffic_multiplier *= 1.5
            
        average_speed = random.uniform(20, 50) / traffic_multiplier # km/h
        intersection_count = int(distance / random.uniform(100, 500))
        road_type = random.choice([1, 2, 3]) # 1: Highway, 2: Arterial, 3: Local
        
        # Base delivery time based on distance and adjusted speed + intersection delays
        base_time_s = (distance / (average_speed * 1000 / 3600)) 
        intersection_delay = intersection_count * random.uniform(5, 15)
        
        delivery_time_s = base_time_s + intersection_delay
        
        # Add some random noise
        delivery_time_s *= random.uniform(0.9, 1.1)
        
        data.append({
            'distance': distance,
            'traffic_multiplier': traffic_multiplier,
            'average_speed': average_speed,
            'hour_of_day': hour_of_day,
            'weather_condition': weather_condition,
            'road_type': road_type,
            'intersection_count': intersection_count,
            'delivery_time': delivery_time_s
        })
        
    df = pd.DataFrame(data)
    
    path = os.path.join(SYNTHETIC_DATA_DIR, "delivery_data.csv")
    df.to_csv(path, index=False)
    print(f"Synthetic data saved to {path}")
    
    return df
