import argparse
import os
import subprocess
from src.simulation import run_simulation

def main():
    parser = argparse.ArgumentParser(description="Delivery ETA and Routing System")
    parser.add_argument('--run-sim', action='store_true', help="Run the CLI simulation")
    parser.add_argument('--city', type=str, default="Hyderabad, Telangana, India", help="City name for simulation")
    parser.add_argument('--traffic', type=str, choices=['low', 'normal', 'high', 'peak'], default='normal', help="Traffic congestion level")
    parser.add_argument('--dashboard', action='store_true', help="Run the Streamlit dashboard")
    
    args = parser.parse_args()
    
    if args.dashboard:
        print("Launching Dashboard...")
        dashboard_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard", "app.py")
        subprocess.run(["streamlit", "run", dashboard_path])
    elif args.run_sim:
        run_simulation(city_name=args.city, congestion_level=args.traffic)
    else:
        print("Please specify an action. Use --help for options.")
        print("Examples:")
        print("  python main.py --run-sim")
        print("  python main.py --dashboard")

if __name__ == "__main__":
    main()
