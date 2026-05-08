from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import os
import subprocess

# --- Section 1: App Initialization ---
app = FastAPI(title="Glaucoma Identification API")

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Section 2: Model Loading or Training ---
MODEL_PATH = "model.pkl"

def get_model():
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Training automatically...")
        # Automatically run the training script
        subprocess.run(["python3", "model_train.py"], check=True)
    
    return joblib.load(MODEL_PATH)

# Global model instance
model = get_model()

# --- Section 3: Data Models ---
class PredictionRequest(BaseModel):
    # This project expects image-based features or binary data.
    # To keep it simple as a "JSON body" request, we accept pre-extracted features.
    # [brightness, disc_size, cup_to_disc_ratio, variation]
    features: list[float]

# --- Section 4: Endpoints ---
@app.post("/predict")
async def predict(request: PredictionRequest):
    try:
        # Prepare data for prediction
        input_data = np.array(request.features).reshape(1, -1)
        
        # Get prediction and probabilities
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
        
        result = "Glaucoma Detected" if prediction == 1 else "Healthy / No Glaucoma"
        confidence = float(probabilities[prediction])
        
        return {
            "prediction": result,
            "confidence": confidence
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"status": "GlaucoVision API is running"}

if __name__ == "__main__":
    import uvicorn
    # Use environment PORT or default to 3000
    port = int(os.environ.get("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)
