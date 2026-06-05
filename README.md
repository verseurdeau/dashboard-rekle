# 🎈 REKLE Dashboard

Sistem cerdas klasifikasi sampah berbasis AI dengan fitur analisis data, prediksi sampah, dan visualisasi interaktif.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

---

## 🚀 Quick Start (Local)

### 1. Setup Dashboard + Model Server (Recommended)

```bash
# Clone & navigate
cd dashboard-rekle

# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r model_server/requirements.txt
```

### 2. Run Model Server (Terminal 1)

```bash
cd model_server
python -m uvicorn app:app --reload --port 8000
```

Cek health: http://localhost:8000/health

### 3. Run Streamlit Dashboard (Terminal 2)

```bash
streamlit run streamlit_app.py
```

Buka: http://localhost:8501

---

## 🐳 Docker Setup (Recommended for Production)

```bash
# Build and run dengan docker-compose
docker-compose up --build

# Dashboard: http://localhost:8501
# API: http://localhost:8000
```

---

## ☁️ Cloud Deployment

### **Option 1: Streamlit Cloud + Railway (Model Server)**

#### Step 1: Deploy Model Server ke Railway

1. Push code ke GitHub
2. Go to https://railway.app
3. Create new project → Deploy from GitHub
4. Select `model_server` folder
5. Set environment variable: `PORT=8000`
6. Copy Railway URL (e.g., `https://your-app.railway.app`)

#### Step 2: Deploy Dashboard ke Streamlit Cloud

1. Go to https://share.streamlit.io
2. Deploy from GitHub
3. Add secret untuk `MODEL_API_URL`:
   - Go to "Settings" → "Secrets"
   - Add:
     ```
     MODEL_API_URL = "https://your-app.railway.app"
     ```

### **Option 2: Both on Railway**

1. Create 2 projects di Railway:
   - Project 1: Model Server (from `model_server/` folder)
   - Project 2: Streamlit (from root folder)
2. Set environment variable di Streamlit project:
   ```
   MODEL_API_URL = https://model-server-project.railway.app
   ```

### **Option 3: Google Cloud Run**

```bash
# Model Server
gcloud run deploy rekle-model \
  --source model_server \
  --platform managed \
  --region us-central1

# Streamlit
gcloud run deploy rekle-dashboard \
  --source . \
  --platform managed \
  --region us-central1
```

---

## 📋 Konfigurasi

### Environment Variables

**Local** (`.streamlit/secrets.toml`):
```toml
MODEL_API_URL = "http://localhost:8000"
```

**Cloud** (Streamlit Settings → Secrets):
```
MODEL_API_URL = "https://your-api-url.com"
```

---

## 📊 Features

| Feature | Local | Cloud |
|---------|:-----:|:-----:|
| 🏠 Home | ✅ | ✅ |
| 📊 Analysis Data | ✅ | ✅ |
| 📈 Model Performance | ✅ | ✅ |
| 🤖 Prediction (API) | ✅ | ✅ |
| 🤖 Prediction (Local TF) | ✅ | ⚠️ |

---

## 🔧 Architecture

```
┌─────────────────────────────────────────┐
│         Streamlit Dashboard             │
│  (Ringan, berjalan di Streamlit Cloud)  │
└──────────────┬──────────────────────────┘
               │ HTTP Request
               │ (Upload Gambar)
               ↓
┌──────────────────────────────────────┐
│    FastAPI Model Server              │
│  (TensorFlow + Model Inference)      │
│  Berjalan di Railway / Cloud Run     │
└──────────────────────────────────────┘
```

---

## 📁 Project Structure

```
dashboard-rekle/
├── streamlit_app.py              # Main dashboard
├── requirements.txt              # Dashboard dependencies
│
├── model_server/
│   ├── app.py                   # FastAPI server
│   ├── requirements.txt          # Server dependencies
│   ├── Dockerfile              # Docker untuk server
│   └── best_model.keras         # Model file
│
├── .streamlit/
│   ├── config.toml              # Streamlit config
│   └── secrets.toml             # Local secrets
│
├── docker-compose.yml           # Local dev setup
├── Dockerfile.streamlit         # Docker untuk dashboard
└── dataset_tabular_clean.csv    # Dataset
```

---

## 🛠️ API Reference

### Health Check

```bash
GET /health
```

Response:
```json
{
  "status": "ok",
  "tensorflow": true,
  "model_loaded": true,
  "classes_loaded": true
}
```

### Predict

```bash
POST /predict
Content-Type: multipart/form-data

Body: file=<image.jpg>
```

Response:
```json
{
  "success": true,
  "class": "Plastik",
  "confidence": 95.42,
  "class_index": 6,
  "all_predictions": {
    "B3": 0.5,
    "Plastik": 95.42,
    ...
  }
}
```

### Get Classes

```bash
GET /classes
```

---

## ⚠️ Troubleshooting

### "Connection refused" error

- Pastikan Model Server berjalan
- Check: `curl http://localhost:8000/health`

### Model loads slowly

- TensorFlow membutuhkan waktu ~30 detik loading pertama kali
- Normal behavior, cache akan mempercepat request berikutnya

### Port 8000 already in use

```bash
# Kill process
lsof -ti:8000 | xargs kill -9

# Atau gunakan port lain
uvicorn app:app --port 8001
```

---

## 📚 Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [TensorFlow Docs](https://www.tensorflow.org)
- [Railway Docs](https://docs.railway.app)
- [Docker Docs](https://docs.docker.com)


