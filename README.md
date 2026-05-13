# Optimizing Delivery ETAs with Graph-Based Network Intelligence

An intelligent delivery routing and ETA prediction system using graph algorithms, real-world map data, dynamic traffic simulation, and machine learning.

This project simulates how companies like Uber, Swiggy, Zomato, and Amazon optimize delivery routes and predict delivery times using a mix of traditional algorithms and modern AI.

## Features
- **Real Road Network Integration**: Downloads real city map data using `OSMnx`.
- **Graph Construction**: Represents roads as weighted directed graphs with distances, speeds, and travel times.
- **Routing Engine**: Implements Dijkstra and A* algorithms to find shortest and dynamic fastest routes.
- **Dynamic Traffic Simulation**: Simulates varying traffic levels (low, normal, high, peak) with random congestion multipliers and road blockages.
- **Machine Learning ETA Prediction**: Uses a `RandomForestRegressor` trained on synthetic delivery data (considering distance, traffic, weather, time of day, and intersections) to accurately predict ETAs.
- **Interactive Dashboard**: A Streamlit dashboard to visualize routes, view statistics, and compare shortest vs fastest routes.

## Architecture & Algorithms
- **Graph Theory**: NetworkX is used to model intersections as nodes and roads as edges. Edge weights dynamically change based on traffic.
- **Shortest Path Algorithms**: Dijkstra's algorithm is applied for the absolute shortest distance route, and for finding the fastest route considering base travel time.
- **Traffic Simulation**: Traffic levels modify the `dynamic_time` attribute of graph edges, triggering route recalculations.
- **ML ETA Model**: Scikit-Learn's `RandomForestRegressor` provides a robust, non-linear prediction model based on rich feature sets simulating real-world conditions.

## Project Structure
```
delivery-eta-system/
├── data/                  # Contains raw, processed, and synthetic data
├── models/                # Trained ML models
├── src/                   # Core modules for graph, traffic, routing, features, ML
├── dashboard/             # Streamlit web app
├── main.py                # Main entry point for CLI and dashboard
└── requirements.txt       # Dependencies
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd delivery-eta-system
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run the CLI Simulation
This will download map data (if not cached), simulate traffic, train the ML model (if not trained), and calculate routes.
```bash
python main.py --run-sim
```

**Options:**
- `--city "City Name, Country"` (Default: "Hyderabad, Telangana, India")
- `--traffic "peak"` (Choices: low, normal, high, peak)

### Launch the Dashboard
Run the interactive Streamlit dashboard to visualize routes and predictions.
```bash
python main.py --dashboard
```

## Future Enhancements
- Real-time traffic API integration (e.g., Google Maps API or TomTom).
- Multi-driver assignment optimization and route batching.
- Reinforcement learning for adaptive route selection.
- Dockerizing the application for easier deployment.
