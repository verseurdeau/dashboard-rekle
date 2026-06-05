# 🎈 REKLE Dashboard

Sistem cerdas klasifikasi sampah berbasis AI dengan fitur analisis data, prediksi sampah, dan visualisasi interaktif.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

1. Create and activate the virtual environment (if not already created):

   ```bash
   cd /workspaces/dashboard-rekle
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the requirements:

   ```bash
   pip install -r requirements.txt
   ```

3. For full functionality (including AI predictions), install TensorFlow:

   ```bash
   pip install tensorflow
   ```

4. Run the app:

   ```bash
   streamlit run streamlit_app.py
   ```

> Jika kamu menggunakan VS Code, pilih interpreter Python:
> `/workspaces/dashboard-rekle/.venv/bin/python`

### Deployment Status

**✅ Streamlit Cloud**: Aplikasi sudah bisa di-deploy!

**Catatan Penting**:
- Fitur **Prediksi Sampah** memerlukan TensorFlow, yang tidak kompatibel dengan Python 3.14 di Streamlit Cloud saat ini
- Fitur **Analisis Data**, **Model Performance**, dan **About REKLE** tersedia penuh
- Untuk menggunakan fitur prediksi, jalankan aplikasi secara lokal setelah menginstal TensorFlow

### Fitur Tersedia

| Fitur | Status | Keterangan |
|-------|--------|-----------|
| 🏠 Home | ✅ | Ringkasan data dan metrik model |
| 📊 Analisis Data | ✅ | Visualisasi dan filter dataset |
| 📈 Model Performance | ✅ | Metrik evaluasi dan classification report |
| 🤖 Prediksi Sampah | ⚠️ Lokal saja | Memerlukan TensorFlow (lokal) |
| 📋 About REKLE | ✅ | Informasi tentang teknologi |

### Troubleshooting

**TensorFlow tidak tersedia di Streamlit Cloud**
- Ini adalah keterbatasan Python 3.14 vs TensorFlow wheel availability
- Solusi: Gunakan aplikasi secara lokal untuk fitur prediksi

**File model/dataset tidak ditemukan**
- Pastikan `best_model.keras`, `dataset_tabular_clean.csv`, dan `class_names.json` tersedia
- Untuk deployment, file-file ini harus di-commit ke git repository

**Memory issues pada deployment**
- Streamlit Cloud memiliki resource terbatas
- Untuk penggunaan production, pertimbangkan hosting di platform dengan resource lebih besar

