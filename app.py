import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ===============================
# 1. PAGE CONFIGURATION
# ===============================
st.set_page_config(
    page_title="Matriks Kinerja Bandara Strategis",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# 2. DESIGN SYSTEM & COLORS
# ===============================
# Palette matched to "Strategic/Trust" theme
PRIMARY = "#0F4C75"   
DANGER = "#3282B8"    
SECONDARY = "#F07B3F" 
ACCENT = "#FFD460"    
SUCCESS = "#28C76F"   
BACKGROUND = "#F4F4F4"

# Matplotlib Global Styling
plt.rcParams["axes.facecolor"] = "#FFFFFF"
plt.rcParams["figure.facecolor"] = "#FFFFFF"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["text.color"] = PRIMARY
plt.rcParams["axes.labelcolor"] = PRIMARY
plt.rcParams["xtick.color"] = PRIMARY
plt.rcParams["ytick.color"] = PRIMARY
plt.rcParams["axes.grid"] = False

# ===============================
# 3. CUSTOM CSS (UI POLISH)
# ===============================
def local_css():
    st.markdown(
        f"""
        <style>
        /* Import Font: Inter (Professional UI font) */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
            color: {PRIMARY};
        }}

        /* --- SIDEBAR STYLING --- */
        [data-testid="stSidebar"] {{
            background-color: {PRIMARY};
            border-right: 1px solid {PRIMARY};
        }}
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
            color: white !important;
        }}
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {{
            color: #E0E0E0 !important;
        }}
        
        /* Custom Radio Buttons as Cards */
        [data-testid="stSidebar"] div[role="radiogroup"] label p {{
            color: {PRIMARY} !important;
            font-weight: 600;
        }}
        div[role="radiogroup"] > label {{
            background-color: white;
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 8px;
            border: 1px solid transparent;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.2s ease;
        }}
        div[role="radiogroup"] > label:hover {{
            background-color: {SECONDARY};
            transform: scale(1.02);
        }}
        div[role="radiogroup"] > label:hover p {{
            color: white !important;
        }}
        /* Active Selection styling */
        div[role="radiogroup"] > label[data-baseweb="radio"] {{
            background-color: #f8f9fa;
            border-left: 6px solid {SECONDARY};
        }}

        /* --- METRIC CARDS --- */
        [data-testid="stMetric"] {{
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            border-top: 4px solid {PRIMARY};
        }}
        [data-testid="stMetricLabel"] {{
            color: #888;
            font-size: 14px;
            font-weight: 600;
        }}
        [data-testid="stMetricValue"] {{
            color: {PRIMARY};
            font-weight: 700;
            font-size: 26px !important;
        }}

        /* --- DATAFRAME STYLING --- */
        [data-testid="stDataFrame"] {{
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            overflow: hidden;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

local_css()

# ===============================
# 4. DATA LOADER
# ===============================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("airport_delay_business_v2.csv")
    except FileNotFoundError:
        st.error("⚠️ Sumber Data Hilang. Pastikan 'airport_delay_business_v2.csv' ada di direktori root.")
        return pd.DataFrame()
    
    # Feature Engineering for Visuals
    df['Delay_Category'] = pd.cut(
        df['total_delay'], 
        bins=[-1, 500, 1500, 1000000], 
        labels=['Efisien', 'Sedang', 'Kritis']
    )
    return df

df = load_data()

# ===============================
# 5. SIDEBAR NAVIGATION
# ===============================
st.sidebar.markdown(f"<h2 style='color: white;'>✈️ Administrasi Penerbangan Federal</h2>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='color: #CCCCCC; font-size: 12px; margin-top: -15px;'>Kantor Intelijen Bandara</p>", unsafe_allow_html=True)

st.sidebar.markdown("### 🧭 Modul Strategis")
selected_view = st.sidebar.radio(
    "Navigasi",
    options=[
        "📊 Benchmark Operasional", 
        "💵 Matriks Efisiensi Biaya", 
        "🌦️ Analisis Akar Penyebab",
        "📈 Tren Volume & Kapasitas"
    ],
    label_visibility="collapsed"
)
st.sidebar.divider()

# --- FILTER SECTION ---
st.sidebar.markdown("### 🎚️ Segmentasi Kohort")

# Year Filter
available_years = sorted(df['year'].unique())
selected_year = st.sidebar.select_slider("Tahun Fiskal", options=available_years, value=available_years[-1])

# Passenger Volume Filter (Safe Handling)
df_clean_passengers = df.dropna(subset=['total_passengers'])
if not df_clean_passengers.empty:
    min_p, max_p = int(df_clean_passengers['total_passengers'].min()), int(df_clean_passengers['total_passengers'].max())
else:
    min_p, max_p = 0, 0

passenger_range = st.sidebar.slider(
    "Volume Penumpang",
    min_value=min_p,
    max_value=max_p,
    value=(min_p, max_p),
    step=1000
)

# Apply Filters
df_filtered = df[
    (df['year'] == selected_year) &
    (df['total_passengers'] >= passenger_range[0]) &
    (df['total_passengers'] <= passenger_range[1])
].copy()

# ===============================
# 6. MAIN DASHBOARD CONTENT
# ===============================


if df_filtered.empty:
    st.warning("⚠️ Tidak ada data tersedia untuk filter yang dipilih. Silakan sesuaikan rentang Volume Penumpang.")
else:
    # --- HEADER ---
    c_title, c_logo = st.columns([5,1])
    with c_title:
        st.markdown(f"<h1 style='margin-bottom:0;'>Matriks Kinerja Bandara Strategis</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{SECONDARY}; font-weight:600; font-size: 1.1em;'>Briefing Intelijen Operasional: TF {selected_year}</p>", unsafe_allow_html=True)
        st.markdown("*Briefing rahasia mengenai keterlambatan operasional, volume penumpang, dan efisiensi harga tiket.*")

    # --- KPI METRICS ---
    st.markdown("### 📊 KPI Nasional")
    m1, m2, m3, m4 = st.columns(4)

    # Global Baseline for Deltas
    avg_delay_national = df['total_delay'].mean()
    curr_delay_avg = df_filtered['total_delay'].mean()
    
    with m1: st.metric("Bandara Dipantau", f"{len(df_filtered)}")
    with m2: 
        st.metric(
            "Rata-rata Total Delay", 
            f"{curr_delay_avg:,.0f} min", 
            delta=f"{curr_delay_avg - avg_delay_national:,.0f} vs Baseline", 
            delta_color="inverse"
        )
    with m3: st.metric("Rata-rata Harga Tiket", f"${df_filtered['avg_fare'].mean():,.2f}")
    with m4: st.metric("Penumpang Diproses", f"{df_filtered['total_passengers'].sum()/1e6:.1f} M")

    st.markdown("---")

    # ==========================
    # MODULE 1: BENCHMARKS
    # ==========================
    if selected_view == "📊 Benchmark Operasional":
        st.subheader("📊 Benchmark Strategis & Peringkat")
        st.markdown("**Ringkasan Eksekutif:** Analisis komparatif efisiensi bandara. Hijau menunjukkan kinerja tinggi (delay rendah).")

        tab1, tab2, tab3 = st.tabs(["🏆 Efisiensi Tinggi", "⚠️ Hub Delay Kritis", "💰 Hub Biaya Tinggi"])
        
        with tab1:
            st.markdown("##### 🏆 10 Bandara Paling Efisien (Delay Rendah)")
            st.dataframe(
                df_filtered[['airport', 'total_delay', 'total_passengers']].sort_values('total_delay').head(10)
                .style.format({"total_delay": "{:,.0f}", "total_passengers": "{:,.0f}"})
                .background_gradient(subset=['total_delay'], cmap='Greens'), 
                use_container_width=True
            )
            
        with tab2:
            st.markdown("##### ⚠️ 10 Hub Delay Kritis")
            st.dataframe(
                df_filtered[['airport', 'total_delay', 'carrier_delay', 'weather_delay']].sort_values('total_delay', ascending=False).head(10)
                .style.format({"total_delay": "{:,.0f}", "carrier_delay": "{:,.0f}"})
                .background_gradient(subset=['total_delay'], cmap='Reds'), 
                use_container_width=True
            )
            
        with tab3:
            st.markdown("##### 💰 10 Bandara Paling Mahal")
            st.dataframe(
                df_filtered[['airport', 'avg_fare', 'total_delay']].dropna(subset=['avg_fare']).sort_values('avg_fare', ascending=False).head(10)
                .style.format({"avg_fare": "${:.2f}", "total_delay": "{:,.0f}"})
                .background_gradient(subset=['avg_fare'], cmap='Oranges'), 
                use_container_width=True
            )
        
        # Charts Row
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Profil Distribusi Delay")
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.histplot(df_filtered['total_delay'], kde=True, color=PRIMARY, ax=ax)
            ax.set_xlabel("Total Delay (Menit)")
            st.pyplot(fig, use_container_width=True)
        with c2:
            st.markdown("#### Korelasi Harga vs. Delay")
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.scatterplot(data=df_filtered, x='avg_fare', y='total_delay', hue='Delay_Category', palette={'Efisien': SUCCESS, 'Sedang': SECONDARY, 'Kritis': DANGER}, ax=ax)
            ax.set_xlabel("Rata-rata Harga Tiket ($)")
            st.pyplot(fig, use_container_width=True)

    # ==========================
    # MODULE 2: COST EFFICIENCY
    # ==========================
    elif selected_view == "💵 Matriks Efisiensi Biaya":
        st.subheader("💵 Matriks Manfaat Biaya")
        st.info("💡 **Arahan Strategis:** Identifikasi bandara 'Bernilai Tinggi' yang memberikan delay rendah meskipun volume penumpang tinggi atau biaya wajar.")

        df_scatter = df_filtered.dropna(subset=['avg_fare', 'total_delay', 'total_passengers'])
        
        if not df_scatter.empty:
            fig3, ax3 = plt.subplots(figsize=(10, 6))
            scatter = ax3.scatter(
                df_scatter["avg_fare"], df_scatter["total_delay"],
                c=df_scatter["total_passengers"], cmap="Blues",
                s=df_scatter["total_passengers"] / 1000, 
                alpha=0.7, edgecolors='black', linewidth=0.5
            )
            
            # Quadrants
            ax3.axvline(df_scatter["avg_fare"].mean(), color='gray', linestyle='--', alpha=0.5)
            ax3.axhline(df_scatter["total_delay"].mean(), color='gray', linestyle='--', alpha=0.5)
            
            ax3.text(df_scatter["avg_fare"].max(), df_scatter["total_delay"].max(), "⚠️ NILAI BURUK\n(Biaya Tinggi, Delay Tinggi)", ha='right', color=DANGER, fontweight='bold')
            ax3.text(df_scatter["avg_fare"].min(), df_scatter["total_delay"].min(), "✅ NILAI TERBAIK\n(Biaya Rendah, Delay Rendah)", ha='left', color=SUCCESS, fontweight='bold')
            
            ax3.set_xlabel("Rata-rata Harga Tiket ($)")
            ax3.set_ylabel("Total Delay (Menit)")
            ax3.set_title("Ukuran Bubble = Volume Penumpang")
            plt.colorbar(scatter, ax=ax3, label='Volume Penumpang')
            st.pyplot(fig3, use_container_width=True)

    # ==========================
    # MODULE 3: ROOT CAUSE
    # ==========================
    elif selected_view == "🌦️ Analisis Akar Penyebab":
        st.subheader("🌦️ Dekomposisi Akar Penyebab Delay")
        
        causes = df_filtered[['carrier_delay', 'weather_delay', 'nas_delay', 'late_aircraft_delay']].sum()
        
        col_a, col_b = st.columns([1, 1])
        with col_a:
            fig4, ax4 = plt.subplots(figsize=(6, 6))
            ax4.pie(causes, labels=['Maskapai', 'Cuaca', 'NAS', 'Pesawat Terlambat'], autopct='%1.1f%%', colors=[PRIMARY, SECONDARY, ACCENT, "#95A5A6"], wedgeprops={'edgecolor': 'white'}, textprops={'color': 'black'})
            ax4.set_title(f"Komposisi Delay (TF {selected_year})")
            st.pyplot(fig4, use_container_width=True)
        with col_b:
            st.markdown("#### 💡 Analisis Insight")
            dominant = causes.idxmax().replace('_delay', '').upper()
            st.metric("Faktor Risiko Dominan", dominant, "Memerlukan Mitigasi")
            st.dataframe(causes.rename("Total Menit"), use_container_width=True)

    # ==========================
    # MODULE 4: VOLUME TRENDS (FIXED)
    # ==========================
    elif selected_view == "📈 Tren Volume & Kapasitas":
        st.subheader("📈 Tes Stress Volume & Kapasitas")
        st.markdown("**Objektif:** Menilai apakah infrastruktur bandara (volume penumpang) adalah pendorong utama dari kegagalan operasional (delay).")

        # Clean Data for Analysis
        df_vol = df_filtered.dropna(subset=['total_passengers', 'total_delay'])

        if df_vol.empty:
            st.warning("Data tidak cukup untuk Analisis Volume.")
        else:
            # 1. Regression Plot
            st.markdown("#### 1. Korelasi: Volume vs. Delays")
            fig5, ax5 = plt.subplots(figsize=(10, 4))
            sns.regplot(x="total_passengers", y="total_delay", data=df_vol, 
                        scatter_kws={'alpha':0.5, 'color': PRIMARY}, line_kws={'color': DANGER}, ax=ax5)
            ax5.set_xlabel("Total Penumpang (Throughput)")
            ax5.set_ylabel("Total Delay (Menit)")
            ax5.grid(True, alpha=0.2)
            st.pyplot(fig5, use_container_width=True)

            # 2. Top Busiest Hubs Status (FIXED & STYLED)
            st.markdown("---")
            st.markdown("#### 2. Top 5 Bandara Tersibuk: Cek Kinerja")
            st.caption("Apakah bandara terbesar juga yang terburuk kinerjanya? Batang merah menunjukkan delay melebihi rata-rata nasional.")
            
            # Get Top 5 Busiest
            top_5_busy = df_vol.sort_values("total_passengers", ascending=False).head(5)
            
            if not top_5_busy.empty:
                fig6, ax6 = plt.subplots(figsize=(10, 5))
                
                # Logic Warna: Merah jika di atas rata-rata nasional, Hijau jika di bawah
                bar_palette = [DANGER if x > avg_delay_national else SUCCESS for x in top_5_busy["total_delay"]]
                
                sns.barplot(
                    data=top_5_busy,
                    x="airport",
                    y="total_delay",
                    palette=bar_palette,
                    ax=ax6
                )
                
                # Garis Rata-rata Nasional
                ax6.axhline(avg_delay_national, color=PRIMARY, linestyle="--", linewidth=2, label=f"Rata-rata Nasional: {avg_delay_national:,.0f} min")
                
                # Labels
                ax6.set_xlabel("Kode Bandara")
                ax6.set_ylabel("Delay Akumulatif (Menit)")
                ax6.legend()
                ax6.grid(axis='y', linestyle=':', alpha=0.3)
                
                st.pyplot(fig6, use_container_width=True)
            else:
                st.info("Tidak ada data tersedia untuk bandara teratas.")

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #888; font-size: 12px;'>
        &copy; 2026 Administrasi Penerbangan Federal | Kantor Strategi Data <br>
        <span style='color:{SECONDARY};'>Sumber Data: Biro Statistik Transportasi (BTS)</span>
    </div>
    """, 
    unsafe_allow_html=True

)
