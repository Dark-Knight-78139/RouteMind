import streamlit as st
import os
import sys
import folium
from streamlit_folium import folium_static
import random

# Add parent directory to path so we can import src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import DEFAULT_CITY, MODELS_DIR
from src.graph_builder import load_graph, download_map, save_graph
from src.traffic_engine import simulate_traffic
from src.routing import find_shortest_route, find_dynamic_route, get_route_stats
from src.eta_model import ETAPredictor
from src.visualization import get_comparison_map

st.set_page_config(page_title="Delivery Routing Intelligence", layout="wide")

st.title("🚚 Optimizing Delivery ETAs with Graph-Based Network Intelligence")
st.markdown("""
This dashboard demonstrates an intelligent routing system that uses **Graph Algorithms**, 
**Dynamic Traffic Simulation**, and **Machine Learning** to find optimal routes and predict delivery times.
""")

@st.cache_resource
def get_city_graph():
    try:
        return load_graph()
    except:
        with st.spinner("Downloading city map... This may take a minute."):
            G = download_map(DEFAULT_CITY)
            save_graph(G)
            return G

@st.cache_resource
def get_predictor():
    p = ETAPredictor()
    model_path = os.path.join(MODELS_DIR, "eta_model.pkl")
    if os.path.exists(model_path):
        p.load()
    return p

G = get_city_graph()
predictor = get_predictor()

# Sidebar
st.sidebar.header("Simulation Settings")
congestion_level = st.sidebar.select_slider(
    "Traffic Congestion Level",
    options=['low', 'normal', 'high', 'peak'],
    value='normal'
)

weather_cond = st.sidebar.selectbox("Weather", ["Clear", "Rain", "Storm"])
weather_map = {"Clear": 0, "Rain": 1, "Storm": 2}

hour = st.sidebar.slider("Hour of Day", 0, 23, 14)

if st.sidebar.button("Generate New Route"):
    # Generate random source and destination
    nodes = list(G.nodes())
    source = random.choice(nodes)
    target = random.choice(nodes)
    while source == target:
        target = random.choice(nodes)
        
    st.session_state['source'] = source
    st.session_state['target'] = target

if 'source' not in st.session_state:
    nodes = list(G.nodes())
    st.session_state['source'] = random.choice(nodes)
    st.session_state['target'] = random.choice(nodes)

# Main Area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Route Visualization")
    
    # Simulate traffic
    G_traffic = simulate_traffic(G, congestion_level)
    
    try:
        source = st.session_state['source']
        target = st.session_state['target']
        
        route_shortest = find_shortest_route(G_traffic, source, target)
        route_dynamic = find_dynamic_route(G_traffic, source, target)
        
        stats_short = get_route_stats(G_traffic, route_shortest)
        stats_dyn = get_route_stats(G_traffic, route_dynamic)
        
        m = get_comparison_map(G_traffic, route_shortest, route_dynamic)
        folium_static(m, width=800, height=500)
        
    except Exception as e:
        st.error(f"Could not find a valid route between these points. Please generate a new route. Error: {e}")

with col2:
    st.subheader("Route Statistics")
    if 'stats_dyn' in locals():
        st.markdown("### 🛣️ Shortest Distance Route")
        st.write(f"**Distance:** {stats_short['distance_m']/1000:.2f} km")
        st.write(f"**Time (in Traffic):** {stats_short['dynamic_time_s']/60:.2f} mins")
        
        st.markdown("### ⚡ Dynamic Fastest Route")
        st.write(f"**Distance:** {stats_dyn['distance_m']/1000:.2f} km")
        st.write(f"**Time (in Traffic):** {stats_dyn['dynamic_time_s']/60:.2f} mins")
        
        time_saved = (stats_short['dynamic_time_s'] - stats_dyn['dynamic_time_s']) / 60
        if time_saved > 0:
            st.success(f"Dynamic routing saves **{time_saved:.2f} mins**!")
        else:
            st.info("Shortest route is also the fastest.")
            
        st.markdown("---")
        st.subheader("🤖 ML ETA Prediction")
        
        if predictor.model:
            # Predict ETA
            features = {
                'distance': stats_dyn['distance_m'],
                'traffic_multiplier': 1.5 if congestion_level == 'high' else (2.5 if congestion_level == 'peak' else 1.0),
                'average_speed': 30.0,
                'hour_of_day': hour,
                'weather_condition': weather_map[weather_cond],
                'road_type': 2,
                'intersection_count': len(route_dynamic)
            }
            
            eta_s = predictor.predict(features)
            st.metric(label="Predicted Delivery Time", value=f"{eta_s/60:.2f} mins")
            
            st.caption("Machine learning model takes into account historical data, distance, traffic multipliers, weather, and intersection delays.")
        else:
            st.warning("Model not trained yet. Run the simulation script to generate data and train the model.")
