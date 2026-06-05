import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

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

@st.cache_data
def load_data():
    try:
        return pd.read_csv("dataset_tabular_clean.csv")
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data()

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("♻️ REKLE")

menu = st.sidebar.radio(
    "Navigasi",
    [
        "🏠 Home",
        "📊 Analisis Data",
        "📈 Model Performance",
        "📋 About REKLE"
    ]
)

st.sidebar.markdown(
    """
    ### Panduan
    - **Home**: ringkasan data, kategori, dan model.
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
# ANALISIS DATA
# =====================================


elif menu == "📊 Analisis Data":

    st.title("📊 Analisis Dataset")

    st.markdown("Analisis mendalam dataset REKLE sesuai pertanyaan bisnis: dampak lingkungan, metode penanganan, dan keseimbangan data.")

    # Tabs untuk pertanyaan bisnis
    tab1, tab2, tab3 = st.tabs([
        "❓ Pertanyaan 1: Dampak Lingkungan",
        "❓ Pertanyaan 2: Metode Penanganan",
        "❓ Pertanyaan 3: Keseimbangan Data"
    ])

    # ========== PERTANYAAN 1: DAMPAK LINGKUNGAN ==========
    with tab1:
        st.subheader("Pertanyaan 1: Bagaimana distribusi dampak lingkungan pada setiap kategori sampah?")
        
        st.markdown("""
        **Tujuan:** Memahami jenis dampak lingkungan yang ditimbulkan oleh setiap kategori sampah 
        dan hubungan antara kategori sampah dengan tingkat risikonya.
        """)

        st.markdown("---")

        # Distribusi dampak keseluruhan
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Distribusi Dampak Lingkungan (Keseluruhan)")
            dampak_count = (
                df["dampak"]
                .value_counts()
                .reset_index()
            )
            dampak_count.columns = ["Dampak", "Jumlah"]
            
            fig_dampak = px.bar(
                dampak_count,
                x="Jumlah",
                y="Dampak",
                orientation="h",
                color="Jumlah",
                color_continuous_scale="Blues",
                title="Total Data per Dampak"
            )
            st.plotly_chart(fig_dampak, use_container_width=True)

        with col2:
            st.markdown("#### Risk Level Distribution")
            risk_count = (
                df["risk_level"]
                .value_counts()
                .reset_index()
            )
            risk_count.columns = ["Risk Level", "Jumlah"]
            risk_order = ["Rendah", "Sedang", "Tinggi"]
            risk_count["Risk Level"] = pd.Categorical(risk_count["Risk Level"], categories=risk_order, ordered=True)
            risk_count = risk_count.sort_values("Risk Level")
            
            fig_risk = px.bar(
                risk_count,
                x="Risk Level",
                y="Jumlah",
                color="Risk Level",
                color_discrete_map={"Rendah": "#90EE90", "Sedang": "#FFD700", "Tinggi": "#FF6B6B"},
                title="Distribusi Tingkat Risiko"
            )
            st.plotly_chart(fig_risk, use_container_width=True)

        # Heatmap: Dampak × Kategori Sampah
        st.markdown("---")
        st.markdown("#### Heatmap: Dampak Lingkungan × Kategori Sampah")
        
        dampak_kategori_cross = pd.crosstab(
            df["kategori_sampah"],
            df["dampak"]
        )
        
        fig_heatmap1 = px.imshow(
            dampak_kategori_cross,
            labels=dict(x="Dampak Lingkungan", y="Kategori Sampah", color="Jumlah"),
            color_continuous_scale="YlOrRd",
            text_auto=True,
            title="Heatmap: Dampak Lingkungan per Kategori Sampah"
        )
        
        fig_heatmap1.update_layout(height=500)
        st.plotly_chart(fig_heatmap1, use_container_width=True)

        st.markdown("""
        **Insight:**
        - Setiap kategori sampah memiliki dampak lingkungan yang berbeda sesuai karakteristik materialnya
        - Kategori **Organik** didominasi oleh dampak "Menghasilkan bau jika menumpuk"
        - Kategori **B3 dan Medis** memiliki dampak paling serius: "Beracun dan berbahaya" dan "Menyebabkan penyakit"
        - Sampah **anorganik** (Plastik, Kaca, Logam, dll) memiliki dampak jangka panjang berupa pencemaran dan penumpukan limbah
        """)

    # ========== PERTANYAAN 2: METODE PENANGANAN ==========
    with tab2:
        st.subheader("Pertanyaan 2: Bagaimana distribusi metode penanganan dan kategori mana yang paling memerlukan pengelolaan khusus?")
        
        st.markdown("""
        **Tujuan:** Mengidentifikasi metode penanganan untuk setiap kategori sampah 
        dan menemukan kategori yang membutuhkan perhatian khusus.
        """)

        st.markdown("---")

        # Alert untuk kategori khusus
        col1, col2 = st.columns(2)

        with col1:
            st.warning("""
            ⚠️ **KATEGORI YANG MEMERLUKAN PENGELOLAAN KHUSUS**
            
            - **B3 (Limbah Berbahaya)**: Memerlukan pembuangan ke tempat pengolahan limbah B3
            - **Medis**: Memerlukan sterilisasi dan pemusnahan khusus
            
            Kedua kategori ini memiliki risiko tertinggi terhadap kesehatan dan lingkungan!
            """)

        with col2:
            b3_data = len(df[df["kelas"] == "B3"])
            medis_data = len(df[df["kelas"] == "medis"])
            st.info(f"""
            📊 **Jumlah Data:**
            
            - B3: {b3_data:,} data ({b3_data/len(df)*100:.1f}%)
            - Medis: {medis_data:,} data ({medis_data/len(df)*100:.1f}%)
            """)

        # Distribusi penanganan keseluruhan
        st.markdown("---")
        st.markdown("#### Distribusi Metode Penanganan (Keseluruhan)")

        penanganan_count = (
            df["penanganan"]
            .value_counts()
            .reset_index()
        )
        penanganan_count.columns = ["Penanganan", "Jumlah"]

        fig_penanganan = px.bar(
            penanganan_count,
            x="Jumlah",
            y="Penanganan",
            orientation="h",
            color="Jumlah",
            color_continuous_scale="Greens",
            title="Total Data per Metode Penanganan"
        )
        st.plotly_chart(fig_penanganan, use_container_width=True)

        # Heatmap: Penanganan × Kategori Sampah
        st.markdown("---")
        st.markdown("#### Heatmap: Metode Penanganan × Kategori Sampah")

        penanganan_kategori_cross = pd.crosstab(
            df["kategori_sampah"],
            df["penanganan"]
        )

        fig_heatmap2 = px.imshow(
            penanganan_kategori_cross,
            labels=dict(x="Metode Penanganan", y="Kategori Sampah", color="Jumlah"),
            color_continuous_scale="Teal",
            text_auto=True,
            title="Heatmap: Metode Penanganan per Kategori Sampah"
        )

        fig_heatmap2.update_layout(height=500)
        st.plotly_chart(fig_heatmap2, use_container_width=True)

        st.markdown("""
        **Insight:**
        - **Organik**: Seluruhnya ditangani melalui pengolahan menjadi kompos
        - **Anorganik**: Didominasi oleh berbagai metode daur ulang (kerajinan, bahan baku, dll)
        - **B3 & Medis**: Memiliki metode penanganan khusus yang berbeda dari sampah lainnya
        - Identifikasi jenis sampah secara akurat sangat penting untuk penanganan yang tepat
        """)

    # ========== PERTANYAAN 3: KESEIMBANGAN DATA ==========
    with tab3:
        st.subheader("Pertanyaan 3: Apakah distribusi data representatif dan seimbang untuk model klasifikasi optimal?")
        
        st.markdown("""
        **Tujuan:** Mengevaluasi keseimbangan distribusi data antar kategori 
        dan memastikan representasi yang memadai untuk pelatihan model.
        """)

        st.markdown("---")

        # Data balance analysis
        kelas_dist = df["kelas"].value_counts().reset_index()
        kelas_dist.columns = ["Kelas", "Jumlah"]
        kelas_dist["Persentase"] = (kelas_dist["Jumlah"] / len(df) * 100).round(2)
        kelas_dist = kelas_dist.sort_values("Jumlah", ascending=False)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Distribusi Data per Kelas Sampah")
            fig_dist = px.bar(
                kelas_dist,
                x="Kelas",
                y="Jumlah",
                color="Jumlah",
                color_continuous_scale="Viridis",
                title="Total Data per Kelas"
            )
            st.plotly_chart(fig_dist, use_container_width=True)

        with col2:
            st.markdown("#### Proporsi Kategori Sampah")
            fig_pie = px.pie(
                kelas_dist,
                names="Kelas",
                values="Jumlah",
                title="Proporsi Data Keseluruhan"
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # Tabel detail distribusi
        st.markdown("---")
        st.markdown("#### Tabel Detail Distribusi Data")
        
        display_df = kelas_dist.copy()
        display_df.columns = ["Kelas", "Jumlah", "Persentase (%)"]
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        # Analisis keseimbangan
        st.markdown("---")
        st.markdown("#### Analisis Keseimbangan Data")

        total_data = len(df)
        nonsampah_pct = (len(df[df["kelas"] == "nonsampah"]) / total_data * 100)
        min_class = kelas_dist["Jumlah"].min()
        max_class = kelas_dist["Jumlah"].max()
        imbalance_ratio = max_class / min_class

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Data",
            f"{total_data:,}"
        )

        col2.metric(
            "Jumlah Kategori",
            f"{len(kelas_dist)}"
        )

        col3.metric(
            "Data Terbanyak",
            f"{max_class:,}",
            f"({nonsampah_pct:.1f}%)"
        )

        col4.metric(
            "Imbalance Ratio",
            f"{imbalance_ratio:.2f}x",
            "Data terbanyak vs terkecil"
        )

        st.warning(f"""
        ⚠️ **CATATAN KESEIMBANGAN DATA**
        
        - **Kategori Nonsampah** mendominasi dengan {nonsampah_pct:.1f}% dari total dataset
        - Ratio ketidakseimbangan: {imbalance_ratio:.2f}x (kategori terbanyak vs terkecil)
        - Semua kategori memiliki ≥ 1.000 data, cukup untuk pelatihan model
        - **Rekomendasi**: Gunakan metrik Precision, Recall, F1-Score untuk evaluasi model
        """)

        st.success("""
        ✅ **KESIMPULAN**
        
        Dataset REKLE memiliki representasi yang cukup baik untuk semua kategori. 
        Meskipun tidak sepenuhnya seimbang, setiap kategori memiliki data yang memadai 
        untuk mendukung pengembangan model klasifikasi yang optimal.
        """)

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