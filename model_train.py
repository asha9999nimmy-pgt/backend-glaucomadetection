import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from PIL import Image, ImageDraw
import os

# --- Section 1: Synthetic Dataset Generation ---
# In a real scenario, you would load thousands of clinical fundus images.
# For this project, we create a synthetic dataset of "disc" and "cup" shapes.
def create_synthetic_fundus_data(samples=200):
    X = []
    y = []
    
    for i in range(samples):
        # 0: Healthy, 1: Glaucoma
        label = np.random.randint(0, 2)
        
        # Simulating Cup-to-Disc ratio
        # Healthy: ratio 0.1 to 0.4
        # Glaucoma: ratio 0.5 to 0.9
        if label == 0:
            ratio = np.random.uniform(0.1, 0.4)
        else:
            ratio = np.random.uniform(0.5, 0.9)
            
        # Create a simple feature vector (simplified for scikit-learn)
        # In a real image model, we'd use pixel values or HOG features.
        # Here we use: [avg_brightness, optic_disc_size, cup_to_disc_ratio, variation]
        features = [
            np.random.normal(120, 10), # Avg brightness
            np.random.normal(50, 5),   # Disc size
            ratio,                     # Cup-to-Disc ratio (Key feature)
            np.random.normal(0.5, 0.1) # Texture variation
        ]
        
        X.append(features)
        y.append(label)
        
    return np.array(X), np.array(y)

# --- Section 2: Model Training ---
def train_model():
    print("Generating synthetic dataset...")
    X, y = create_synthetic_fundus_data(500)
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier...")
    # Using RandomForest as requested (sklearn only)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # --- Section 3: Evaluation ---
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    
    # --- Section 4: Saving Model ---
    print("Saving model to model.pkl...")
    joblib.dump(model, 'model.pkl')
    print("Training complete.")

if __name__ == "__main__":
    train_model()
