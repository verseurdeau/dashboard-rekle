# 🚀 Panduan Deploy Terpisah (Separate Hosting Guide)

## 📋 Overview

Aplikasi REKLE Dashboard sekarang menggunakan **arsitektur dua-tier**:
- **Tier 1**: Streamlit Dashboard (UI) - berjalan di Streamlit Cloud
- **Tier 2**: FastAPI Model Server (AI) - berjalan di platform cloud terpisah

---

## 🏃 Quick Deploy (5 menit)

### Step 1: Push ke GitHub ✅

```bash
# Sudah dilakukan!
git push
```

### Step 2: Deploy Model Server ke Railway

1. **Buka**: https://railway.app → Sign in/Sign up dengan GitHub
2. **Create New Project**
3. **Deploy from GitHub**:
   - Select repository: `dashboard-rekle`
   - Root directory: `model_server` ← **PENTING**
4. **Konfigurasi**:
   - Nama: `rekle-model-server`
   - Port otomatis: `8000`
5. **Deploy** → Tunggu ~2 menit
6. **Copy Domain**: Lihat di tab "Settings" (e.g., `https://rekle-model-server-xxx.railway.app`)

### Step 3: Deploy Dashboard ke Streamlit Cloud

1. **Buka**: https://share.streamlit.io → Sign in dengan GitHub
2. **Deploy new app**:
   - Repository: `verseurdeau/dashboard-rekle`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
3. **Advanced settings** (jika perlu) → Pilih Python 3.11
4. **Deploy** → Tunggu ~2 menit

### Step 4: Konfigurasi API URL

1. **Buka** Streamlit Cloud dashboard untuk app kamu
2. **Klik Settings** (⚙️) → **Secrets**
3. **Tambah secret**:
   ```
   MODEL_API_URL = "https://rekle-model-server-xxx.railway.app"
   ```
4. **Rerun** aplikasi (atau tunggu ~5 menit untuk auto-reload)

### ✅ Selesai!

Akses dashboard: https://your-streamlit-domain.streamlit.app

---

## 🔄 Debugging Deployment

### Cek Health Model Server

```bash
# Ganti dengan URL kamu
curl https://your-api-url.railway.app/health

# Respons yang diharapkan:
# {"status": "ok", "tensorflow": true, "model_loaded": true, "classes_loaded": true}
```

### Lihat Logs

**Railway**:
- Dashboard → project → "Deployments" → "View Logs"

**Streamlit Cloud**:
- Dashboard → app → "Manage app" → "Logs"

---

## 📱 Testing Lokal (Sebelum Deploy)

### Terminal 1: Start Model Server

```bash
cd model_server
pip install -r requirements.txt
python -m uvicorn app:app --reload --port 8000
```

### Terminal 2: Start Streamlit

```bash
pip install -r requirements.txt
MODEL_API_URL="http://localhost:8000" streamlit run streamlit_app.py
```

### Test Prediksi

1. Buka http://localhost:8501
2. Ke "Prediksi Sampah" tab
3. Upload gambar
4. Lihat hasil real-time

---

## ⚙️ Alternative Platforms

### Option A: Google Cloud Run (Free tier available)

**Model Server**:
```bash
gcloud run deploy rekle-model \
  --source model_server \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi
```

**Streamlit Secret**:
```
MODEL_API_URL = "https://rekle-model-XXXXX-uc.a.run.app"
```

### Option B: Render (Paid, more reliable)

1. https://render.com → Connect GitHub
2. Create New → Web Service
3. Build from: Select `model_server` branch
4. Environment: Python 3.11
5. Build command: `pip install -r requirements.txt`
6. Start command: `uvicorn app:app --host 0.0.0.0 --port 8000`
7. Deploy

### Option C: Local Docker + ngrok (untuk testing)

```bash
# Terminal 1: Docker
docker-compose up model-server

# Terminal 2: Expose dengan ngrok
ngrok http 8000
# Copy https://xxxx-xx-xxx-xxx.ngrok.io

# Terminal 3: Streamlit
MODEL_API_URL="https://xxxx-xx-xxx-xxx.ngrok.io" streamlit run streamlit_app.py
```

---

## 🐛 Common Issues

### ❌ "Connection refused"
- Model server belum deploy
- Check Railway/Cloud Run logs
- Verify `MODEL_API_URL` correct

### ❌ "502 Bad Gateway"
- Server crash/memory issue
- Check logs: Railway → Deployments → View Logs
- Increase memory: Railway settings → Restart

### ❌ "Model loading timeout"
- TensorFlow memerlukan waktu ~30s pertama kali
- Normal! API juga cache setelahnya
- Check: Tunggu 2 menit, refresh page

### ❌ "Image upload stuck"
- File terlalu besar (max 200MB)
- Internet connection lambat
- Try: Ukuran file < 5MB

---

## 📊 Monitoring

### Railway Logs

```bash
# Real-time logs
railway logs -f

# Filter errors
railway logs | grep ERROR
```

### Health Check

Buat script untuk monitoring:

```python
import requests
import time

API_URL = "https://your-api-url.railway.app"

while True:
    try:
        r = requests.get(f"{API_URL}/health", timeout=5)
        status = r.json()
        print(f"✓ API: OK | TF: {status['tensorflow']} | Model: {status['model_loaded']}")
    except Exception as e:
        print(f"✗ API: {str(e)}")
    
    time.sleep(30)
```

---

## 🔐 Security Notes

- **Secrets**: Jangan commit `MODEL_API_URL` ke git
- **CORS**: API membolehkan request dari domain apapun
- **Auth**: Untuk production, tambahkan API key/auth
- **Rate Limit**: Pertimbangkan untuk deploy with rate limiting

---

## 📝 Ringkasan Arsitektur

```
┌──────────────────────────┐
│   Streamlit Cloud        │
│  • Dashboard UI          │
│  • Analytics             │
│  • Predictions (via API) │
│                          │
│  https://app.streamlit.app
└────────────┬─────────────┘
             │ HTTPS
             │ POST /predict
             │ (with image)
             ↓
┌──────────────────────────┐
│   Railway / GCP / Render │
│  • FastAPI Server        │
│  • TensorFlow Model      │
│  • Model Inference       │
│                          │
│  https://api.railway.app │
└──────────────────────────┘
```

---

## ✅ Checklist Deployment

- [ ] Push ke GitHub
- [ ] Deploy model server ke Railway/GCP/Render
- [ ] Copy API URL
- [ ] Tambah `MODEL_API_URL` secret di Streamlit Cloud
- [ ] Test health check: `/health`
- [ ] Upload test image di dashboard
- [ ] Verify prediksi berfungsi
- [ ] Monitor logs untuk errors

---

## 🆘 Support

**Error di Model Server?**
- Check `/health` endpoint
- Lihat Railway/GCP logs
- Pastikan file `best_model.keras` ada

**Error di Streamlit?**
- Check `MODEL_API_URL` di secrets
- Lihat Streamlit Cloud logs
- Test lokal dengan `curl http://localhost:8000/health`

---

Enjoy! 🎉
