import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image
import json
import requests

# Try importing TensorFlow - optional for deployment
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

# Konfigurasi API Model Server
# Set environment variable atau hardcode untuk production
MODEL_API_URL = st.secrets.get("MODEL_API_URL", "http://localhost:8000")
USE_API = True  # Set False untuk menggunakan model lokal

# =====================================
# CONFIG
# =====================================

st.set_page_config(
    page_title="REKLE Dashboard",
    page_icon="♻️",
    layout="wide"
)


# =====================================
# LOAD DATA
# =====================================

@st.cache_resource
def load_model():
    if not TENSORFLOW_AVAILABLE:
        return None
    try:
        return tf.keras.models.load_model("best_model.keras")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

@st.cache_data
def load_data():
    try:
        return pd.read_csv("dataset_tabular_clean.csv")
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

model = load_model()
df = load_data()

try:
    with open("class_names.json", "r") as f:
        class_names = json.load(f)
except Exception as e:
    st.error(f"Error loading class names: {e}")
    class_names = {}

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("♻️ REKLE")

menu = st.sidebar.radio(
    "Navigasi",
    [
        "🏠 Home",
        "🤖 Prediksi Sampah",
        "📊 Analisis Data",
        "📈 Model Performance",
        "📋 About REKLE"
    ]
)

st.sidebar.markdown(
    """
    ### Panduan
    - **Home**: ringkasan data, kategori, dan model.
    - **Prediksi Sampah**: unggah gambar untuk klasifikasi.
    - **Analisis Data**: visualisasi distribusi dan filter interaktif.
    - **Model Performance**: metrik evaluasi dan laporan klasifikasi.
    - **About REKLE**: informasi teknologi dan fitur.
    """
)

# Check if data and model loaded successfully
if df is None or df.empty:
    st.error("⚠️ Dataset tidak dapat dimuat. Pastikan file 'dataset_tabular_clean.csv' ada di direktori proyek.")
    st.stop()

# =====================================
# HOME
# =====================================

if menu == "🏠 Home":

    st.title("♻️ REKLE Dashboard")

    st.markdown("""
    Selamat datang di REKLE — platform pengelolaan sampah cerdas dengan
    klasifikasi AI, rekomendasi penanganan, dan insight lingkungan.
    """)

    st.markdown("**Data ini membantu Anda memahami jenis sampah, risiko, dan metode penanganan terbaik.**")

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Data",
        f"{len(df):,}"
    )

    col2.metric(
        "Kategori Kelas",
        df["kelas"].nunique()
    )

    col3.metric(
        "Kategori Sampah",
        df["kategori_sampah"].nunique()
    )

    col4.metric(
        "Akurasi Model",
        "95.63%"
    )

    st.markdown("---")

    st.subheader("Sorotan Utama")

    left, right = st.columns([2, 1])

    with left:
        st.markdown(
            """
            - **Kelas sampah** mencakup 9 kategori utama.
            - **Risk Level** membantu menentukan prioritas penanganan.
            - **Dampak lingkungan** menunjukkan konsekuensi tiap kategori.
            """
        )

    with right:
        st.info(
            "Gunakan menu di sebelah kiri untuk berpindah antar fitur dan menemukan informasi dengan cepat."
        )

    st.markdown("---")

    st.subheader("Pratinjau Dataset")

    with st.expander("Lihat 10 baris data teratas"):
        st.dataframe(df.head(10), use_container_width=True)

# =====================================
# PREDIKSI
# =====================================

elif menu == "🤖 Prediksi Sampah":

    st.title("🤖 Klasifikasi Sampah")

    st.markdown("Upload gambar sampah untuk mendapatkan prediksi klasifikasi dan informasi penanganan.")

    uploaded_file = st.file_uploader(
        "Upload gambar sampah",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:

        image = Image.open(uploaded_file).convert("RGB")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.image(
                image,
                caption="Gambar yang diupload",
                use_container_width=True
            )

        with col2:
            # Prediction via API
            if USE_API:
                with st.spinner("🔄 Memproses prediksi..."):
                    try:
                        # Prepare file untuk API
                        files = {"file": uploaded_file.getvalue()}
                        response = requests.post(
                            f"{MODEL_API_URL}/predict",
                            files={"file": (uploaded_file.name, uploaded_file.getvalue())},
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            if result.get("success"):
                                predicted_class = result["class"]
                                confidence = result["confidence"]
                                
                                st.success(f"✅ Prediksi: {predicted_class}")
                                st.metric("Confidence", f"{confidence:.2f}%")
                                
                                # Get metadata dari dataset
                                metadata = df[
                                    df["kelas"].str.lower() == predicted_class.lower()
                                ]
                                
                                if not metadata.empty:
                                    metadata = metadata.iloc[0]
                                    
                                    st.info(
                                        f"""
                                        **Kategori Sampah**
                                        
                                        {metadata['kategori_sampah']}
                                        """
                                    )
                                    
                                    st.warning(
                                        f"""
                                        **Risk Level**
                                        
                                        {metadata['risk_level']}
                                        """
                                    )
                                    
                                    st.success(
                                        f"""
                                        **Penanganan**
                                        
                                        {metadata['penanganan']}
                                        """
                                    )
                                    
                                    st.error(
                                        f"""
                                        **Dampak Lingkungan**
                                        
                                        {metadata['dampak']}
                                        """
                                    )
                            else:
                                st.error(f"❌ Error: {result.get('detail', 'Unknown error')}")
                        else:
                            st.error(f"❌ Server error: {response.status_code}")
                    
                    except requests.exceptions.ConnectionError:
                        st.error(
                            f"""
                            ❌ Tidak bisa menghubungi Model Server.
                            
                            Pastikan server berjalan di: {MODEL_API_URL}
                            
                            Untuk test lokal:
                            ```bash
                            cd model_server
                            python -m uvicorn app:app --reload
                            ```
                            """
                        )
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            
            # Fallback: Local prediction jika TensorFlow tersedia
            else:
                if not TENSORFLOW_AVAILABLE or model is None:
                    st.error("⚠️ Model tidak tersedia (TensorFlow tidak terinstall)")
                    st.stop()
                
                try:
                    img = image.resize((224, 224))
                    img_array = np.array(img, dtype=np.float32)
                    img_array = img_array / 255.0
                    img_array = np.expand_dims(img_array, axis=0)
                    
                    prediction = model.predict(img_array, verbose=0)
                    predicted_idx = np.argmax(prediction)
                    predicted_class = class_names[str(predicted_idx)]
                    confidence = float(np.max(prediction)) * 100
                    
                    st.success(f"✅ Prediksi: {predicted_class}")
                    st.metric("Confidence", f"{confidence:.2f}%")
                    
                    metadata = df[
                        df["kelas"].str.lower() == predicted_class.lower()
                    ]
                    
                    if not metadata.empty:
                        metadata = metadata.iloc[0]
                        
                        st.info(
                            f"""
                            **Kategori Sampah**
                            
                            {metadata['kategori_sampah']}
                            """
                        )
                        
                        st.warning(
                            f"""
                            **Risk Level**
                            
                            {metadata['risk_level']}
                            """
                        )
                        
                        st.success(
                            f"""
                            **Penanganan**
                            
                            {metadata['penanganan']}
                            """
                        )
                        
                        st.error(
                            f"""
                            **Dampak Lingkungan**
                            
                            {metadata['dampak']}
                            """
                        )
                
                except Exception as e:
                    st.error(f"Error prediksi: {e}")

# =====================================
# ANALISIS DATA
# =====================================

elif menu == "📊 Analisis Data":

    st.title("📊 Analisis Dataset")

    st.markdown("Data interaktif dengan filter untuk mengeksplorasi kategori, dampak, dan risiko sampah.")

    kategori_filter = st.multiselect(
        "Filter Kategori Sampah",
        options=sorted(df["kategori_sampah"].dropna().unique()),
        default=sorted(df["kategori_sampah"].dropna().unique())
    )

    risk_filter = st.multiselect(
        "Filter Risk Level",
        options=sorted(df["risk_level"].dropna().unique()),
        default=sorted(df["risk_level"].dropna().unique())
    )

    filtered_df = df[
        (df["kategori_sampah"].isin(kategori_filter))
        &
        (df["risk_level"].isin(risk_filter))
    ]

    total_filtered = len(filtered_df)
    filtered_kelas = filtered_df["kelas"].nunique()
    filtered_risiko = filtered_df["risk_level"].nunique()

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Data Dipilih", f"{total_filtered:,}")
    m2.metric("Kelas Terpilih", filtered_kelas)
    m3.metric("Tingkat Risiko", filtered_risiko)

    st.markdown("---")

    st.subheader("Distribusi Kelas Sampah")

    kelas_count = (
        filtered_df["kelas"]
        .value_counts()
        .reset_index()
    )

    kelas_count.columns = [
        "Kelas",
        "Jumlah"
    ]

    fig1 = px.bar(
        kelas_count,
        x="Kelas",
        y="Jumlah",
        color="Kelas",
        title="Jumlah per Kelas Sampah",
        labels={"Jumlah": "Total", "Kelas": "Kategori"}
    )

    kategori_count = (
        filtered_df["kategori_sampah"]
        .value_counts()
        .reset_index()
    )

    kategori_count.columns = [
        "Kategori",
        "Jumlah"
    ]

    fig2 = px.pie(
        kategori_count,
        names="Kategori",
        values="Jumlah",
        hole=0.4,
        title="Proporsi Kategori Sampah"
    )

    col1, col2 = st.columns(2)
    col1.plotly_chart(fig1, use_container_width=True)
    col2.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    st.subheader("Distribusi Dampak Lingkungan")

    dampak_count = (
        filtered_df["dampak"]
        .value_counts()
        .reset_index()
    )

    dampak_count.columns = [
        "Dampak",
        "Jumlah"
    ]

    fig3 = px.bar(
        dampak_count,
        x="Dampak",
        y="Jumlah"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.subheader("Distribusi Metode Penanganan")

    penanganan_count = (
        filtered_df["penanganan"]
        .value_counts()
        .reset_index()
    )

    penanganan_count.columns = [
        "Penanganan",
        "Jumlah"
    ]

    fig4 = px.bar(
        penanganan_count,
        x="Penanganan",
        y="Jumlah"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    st.subheader("Distribusi Risk Level")

    risk_count = (
        filtered_df["risk_level"]
        .value_counts()
        .reset_index()
    )

    risk_count.columns = [
        "Risk Level",
        "Jumlah"
    ]

    fig5 = px.bar(
        risk_count,
        x="Risk Level",
        y="Jumlah",
        color="Risk Level",
        title="Jumlah per Risk Level",
        labels={"Jumlah": "Total", "Risk Level": "Tingkat Risiko"}
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

    st.markdown("---")
    st.subheader("Tabel Data Filter")
    with st.expander("Lihat data hasil filter"):
        st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

# =====================================
# MODEL PERFORMANCE
# =====================================

elif menu == "📈 Model Performance":

    st.title("📈 Model Performance")

    col1,col2,col3,col4 = st.columns(4)

    col1.metric(
        "Accuracy",
        "95.63%"
    )

    col2.metric(
        "Precision",
        "96.16%"
    )

    col3.metric(
        "Recall",
        "94.95%"
    )

    col4.metric(
        "AUC",
        "99.60%"
    )

    report = pd.DataFrame({
        "Kelas":[
            "B3",
            "Kaca",
            "Kardus",
            "Kertas",
            "Logam",
            "Medis",
            "Plastik",
            "Nonsampah",
            "Organik"
        ],
        "Precision":[
            0.89,0.92,0.93,0.93,0.88,
            0.92,0.90,0.99,0.99
        ],
        "Recall":[
            0.94,0.95,0.86,0.94,0.94,
            0.92,0.90,0.98,0.99
        ],
        "F1-Score":[
            0.91,0.93,0.90,0.94,0.91,
            0.92,0.90,0.99,0.99
        ]
    })

    st.subheader("Classification Report")

    st.dataframe(
        report,
        use_container_width=True
    )

# =====================================
# ABOUT
# =====================================

elif menu == "📋 About REKLE":

    st.title("📋 About REKLE")

    st.markdown("""
    ### REKLE

    REKLE adalah sistem cerdas pilah sampah berbasis Artificial Intelligence
    yang memanfaatkan model Convolutional Neural Network (CNN) untuk
    mengklasifikasikan jenis sampah berdasarkan citra.

    ### Fitur

    - Klasifikasi sampah otomatis
    - Analisis dampak lingkungan
    - Rekomendasi penanganan sampah
    - Analisis data sampah
    - Visualisasi data interaktif

    ### Teknologi

    - TensorFlow
    - MobileNetV2
    - Streamlit
    - Pandas
    - Plotly
    """)