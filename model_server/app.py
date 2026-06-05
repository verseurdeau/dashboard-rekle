"""
Model Server - FastAPI untuk hosting model TensorFlow
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import io
import json
import os

# Try importing TensorFlow
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

app = FastAPI(
    title="REKLE Model API",
    description="API untuk prediksi klasifikasi sampah",
    version="1.0.0"
)

# Enable CORS untuk Streamlit Cloud
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model saat startup
model = None
class_names = {}

@app.on_event("startup")
async def load_resources():
    global model, class_names
    
    if not TF_AVAILABLE:
        print("⚠️ TensorFlow tidak tersedia")
        return
    
    try:
        # Load model
        model_path = "best_model.keras"
        if os.path.exists(model_path):
            model = tf.keras.models.load_model(model_path)
            print(f"✓ Model loaded: {model_path}")
        else:
            print(f"⚠️ Model tidak ditemukan: {model_path}")
        
        # Load class names
        classes_path = "class_names.json"
        if os.path.exists(classes_path):
            with open(classes_path, "r") as f:
                class_names = json.load(f)
            print(f"✓ Class names loaded: {len(class_names)} classes")
        else:
            print(f"⚠️ Class names tidak ditemukan: {classes_path}")
    
    except Exception as e:
        print(f"❌ Error loading resources: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "tensorflow": TF_AVAILABLE,
        "model_loaded": model is not None,
        "classes_loaded": len(class_names) > 0
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Prediksi klasifikasi sampah dari gambar
    
    Args:
        file: Gambar dalam format JPG/PNG
    
    Returns:
        {
            "class": "Nama Kelas",
            "confidence": 95.5,
            "all_predictions": {...}
        }
    """
    
    if not TF_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="TensorFlow tidak tersedia di server"
        )
    
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model belum di-load"
        )
    
    if not class_names:
        raise HTTPException(
            status_code=503,
            detail="Class names belum di-load"
        )
    
    try:
        # Baca gambar
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # Resize ke ukuran model
        image = image.resize((224, 224))
        
        # Convert ke numpy array dan normalize
        img_array = np.array(image, dtype=np.float32)
        img_array = img_array / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        # Predict
        predictions = model.predict(img_array, verbose=0)
        
        # Get top prediction
        predicted_idx = np.argmax(predictions[0])
        predicted_class = class_names[str(predicted_idx)]
        confidence = float(predictions[0][predicted_idx]) * 100
        
        # Get all predictions
        all_predictions = {
            class_names[str(i)]: float(predictions[0][i]) * 100
            for i in range(len(class_names))
        }
        
        return {
            "success": True,
            "class": predicted_class,
            "confidence": round(confidence, 2),
            "class_index": int(predicted_idx),
            "all_predictions": all_predictions
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing image: {str(e)}"
        )

@app.get("/classes")
async def get_classes():
    """Get list of available classes"""
    return {
        "classes": class_names,
        "count": len(class_names)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
