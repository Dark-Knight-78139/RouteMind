import os

# Project configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
SYNTHETIC_DATA_DIR = os.path.join(DATA_DIR, "synthetic")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Default city for the project
DEFAULT_CITY = "Hyderabad, Telangana, India"

def ensure_dirs():
    """Ensure all required directories exist."""
    dirs = [RAW_DATA_DIR, PROCESSED_DATA_DIR, SYNTHETIC_DATA_DIR, MODELS_DIR]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

ensure_dirs()
