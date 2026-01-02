# ✈️ Strategic Airport Performance Analysis: Big Data Approach


> **Project Big Data Analytics** > Proyek analisis komprehensif untuk mengidentifikasi faktor penyebab keterlambatan penerbangan dan strategi mitigasinya menggunakan PySpark dan Streamlit.

---

## 👨‍💻 Profil Mahasiswa
**Nama:** Brilly Jalu Kumara Biseka 
**NIM:** 25917018
**Mata Kuliah:** Big Data Analytics  
**Topik:** Transportasi Udara (Aviation)

---

## 📋 Daftar Isi (Assignment Roadmap)
Dokumen ini disusun berdasarkan 6 poin petunjuk pengerjaan UAS:
1.  [Domain Pilihan](#1-domain-pilihan-%EF%B8%8F)
2.  [Pertanyaan Bisnis](#2-keputusan-organisasi-pertanyaan-bisnis-)
3.  [Sumber Data](#3-kebutuhan-data-sumber-)
4.  [Metodologi Analisis (PySpark)](#4-implementasi-analisis-big-data-pyspark-)
5.  [Dashboard Visualisasi](#5-rancangan-dashboard-visualisasi-)
6.  [Cara Menjalankan Project](#6-cara-menjalankan-project-)

---

### 1. Domain Pilihan 🛫
Saya memilih domain **Transportasi Udara (Aviation Industry)**.
Sektor ini menghasilkan data dalam volume besar (*high volume*) dan kecepatan tinggi (*high velocity*) setiap harinya, menjadikannya kandidat ideal untuk analisis Big Data guna meningkatkan efisiensi operasional.

### 2. Keputusan Organisasi (Pertanyaan Bisnis) ❓
Dalam manajemen bandara dan maskapai, keputusan strategis yang perlu didukung data adalah:

> **"Apa faktor dominan yang menyebabkan keterlambatan (delay) parah di bandara utama, dan bagaimana strategi pengelolaan kapasitas input penerbangan ke depan?"**

**Tujuan:**
* Mengetahui apakah kita perlu membatasi jumlah penerbangan atau menambah infrastruktur.
* Memprediksi risiko delay berdasarkan profil bandara (Volume Penumpang & Harga Tiket).

### 3. Kebutuhan Data & Sumber 📂
Untuk menjawab pertanyaan di atas, saya menggunakan **2 sumber data berbeda** yang kemudian digabungkan (*joined*):

| No | Nama Dataset | Deskripsi | Sumber |
| :-- | :--- | :--- | :--- |
| 1. | **`Airline_Delay_Cause.csv`** | Data operasional yang berisi durasi delay dan penyebabnya (Cuaca, Carrier, NAS, dll). | https://www.kaggle.com/datasets/abdelazizel7or/airline-delay-cause |
| 2. | **`Routes_and_Fares.csv`** | Data bisnis yang berisi rute, harga tiket (*Fare*), dan volume penumpang. | http://kaggle.com/datasets/bhavikjikadara/us-airline-flight-routes-and-fares-1993-2024 |

**Proses Data:**
Data operasional di-*agregasi* per tahun dan per bandara, lalu di-*join* dengan data bisnis untuk mendapatkan pandangan holistik 360 derajat.

### 4. Implementasi Analisis Big Data (PySpark) 🤖
Analisis dilakukan menggunakan **Apache Spark (PySpark)** untuk menangani pemrosesan data skala besar.

#### 🛠️ Tahapan Analisis:
1.  **Data Ingestion:** Membaca file CSV mentah ke dalam Spark DataFrame.
2.  **Preprocessing & Cleaning:** Mengatasi *missing values* dan *casting* tipe data.
3.  **Aggregation:** Menghitung total delay kumulatif per bandara.
4.  **Data Joining:** Menggabungkan dataset Delay dan Fare berdasarkan `Airport Code` dan `Year`.
5.  **Machine Learning (Logistic Regression):**
    * *Target:* Mengklasifikasikan bandara menjadi **"High Delay"** vs **"Normal"**.
    * *Features:* Volume Penumpang & Rata-rata Harga Tiket.

#### 📈 Hasil Analisis:
* **Akurasi Model:** **78.06%** (Model cukup andal untuk prediksi).
* **Insight Koefisien:**
    * `Total Passengers` memiliki korelasi **Positif Kuat** (+0.00017) terhadap delay.
    * Artinya: **Semakin padat bandara, semakin tinggi risiko delay.**
    * Harga tiket juga berbanding lurus, mengindikasikan bandara sibuk/mahal cenderung lebih sering delay.

*(Script lengkap dapat dilihat pada file `Analysis_PySpark.ipynb`)*

### 5. Rancangan Dashboard Visualisasi 📊
Untuk mempermudah stakeholder memahami hasil analisis, saya merancang dashboard interaktif menggunakan **Streamlit**.

**Fitur Utama Dashboard:**
* **Operational Benchmarks:** Ranking bandara paling efisien vs paling macet.
* **Cost-Efficiency Matrix (Scatter Plot):** Kuadran untuk melihat bandara mana yang "High Value" (Murah & Cepat) vs "Low Value".
* **Root Cause Analysis (Pie Chart):** Breakdown penyebab delay (Carrier vs Weather vs NAS).
* **Volume Stress Test:** Regresi linear untuk melihat dampak kenaikan penumpang terhadap delay.

---

### 6. Cara Menjalankan Project 🚀

Ikuti langkah berikut untuk menjalankan analisis dan dashboard di komputer lokal Anda:

**Persiapan Lingkungan:**
Pastikan Python dan library berikut sudah terinstal:
```bash
pip install pyspark streamlit pandas seaborn matplotlib
