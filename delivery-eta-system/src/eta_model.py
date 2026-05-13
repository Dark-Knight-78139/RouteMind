import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
import os
from src.utils import MODELS_DIR

class ETAPredictor:
    def __init__(self, model_path=None):
        if model_path is None:
            self.model_path = os.path.join(MODELS_DIR, "eta_model.pkl")
        else:
            self.model_path = model_path
        self.model = None

    def train(self, data_path):
        print(f"Loading data from {data_path}...")
        df = pd.read_csv(data_path)
        
        features = ['distance', 'traffic_multiplier', 'average_speed', 'hour_of_day', 
                    'weather_condition', 'road_type', 'intersection_count']
        target = 'delivery_time'
        
        X = df[features]
        y = df[target]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print("Training RandomForestRegressor...")
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        predictions = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        
        print(f"Model trained. Mean Absolute Error: {mae:.2f} seconds ({mae/60:.2f} minutes)")
        
        self.save()
        return mae
        
    def save(self):
        joblib.dump(self.model, self.model_path)
        print(f"Model saved to {self.model_path}")
        
    def load(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            print(f"Model loaded from {self.model_path}")
        else:
            raise FileNotFoundError(f"Model file not found at {self.model_path}")
            
    def predict(self, features_dict):
        """
        features_dict expects: distance, traffic_multiplier, average_speed, 
        hour_of_day, weather_condition, road_type, intersection_count
        """
        if self.model is None:
            self.load()
            
        df = pd.DataFrame([features_dict])
        prediction = self.model.predict(df)[0]
        return prediction
