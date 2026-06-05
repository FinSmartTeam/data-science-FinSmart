# FinSmart: Data Science & Analytics Hub

Selamat datang di repositori Data Science proyek FinSmart. Repositori ini mendokumentasikan seluruh proses analisis data secara end-to-end, mulai dari penemuan masalah (Problem Discovery), pengolahan data, pemodelan, pengujian hipotesis, hingga visualisasi dashboard interaktif.

---

## Ringkasan Eksekutif & Solusi Proyek
FinSmart adalah aplikasi web pengelola keuangan berbasis AI untuk meningkatkan literasi finansial generasi muda Indonesia. Platform ini mengintegrasikan machine learning dan analisis keuangan personal untuk pencatatan transaksi yang cerdas dan berkelanjutan. 

Keunggulan utamanya ada pada fitur Financial Behavior (klasifikasi hemat/boros via ML) dan Analisis Kesiapan Investasi. Inovasinya terletak pada otomatisasi rasio keuangan (BLR & SR) untuk memberi saran kapan pengguna aman mulai berinvestasi—sebuah fitur pionir yang belum diterapkan oleh aplikasi pengelola keuangan lainnya.

---

## Struktur Repositori & Cakupan Tugas

Proyek ini dibagi menjadi beberapa modul utama sesuai dengan alur kerja Data Science:

### 1. [Exploratory Data Analysis (EDA)](./EDA)
Fokus pada pengumpulan, pembersihan data, dan pencarian pola awal:
* Data Wrangling: Proses End-to-End yang mencakup Gathering Data (Kaggle dataset), Assessing Data (cek duplikasi & missing values), serta Cleaning Data.
* Data Dictionary: Panduan definisi variabel finansial (Income, Needs, Wants, Savings).
* Exploratory Data Analysis: Analisis tren pengeluaran bulanan, pengeluaran harian (weekday), dan visualisasi distribusi kategori transaksi.

### 2. [A/B Testing](./A%20B%20Testing)
Fokus pada validasi bisnis secara ilmiah menggunakan Python:
* Pengujian Hipotesis: Mengimplementasikan eksperimen A/B Testing untuk mengukur efektivitas sistem rekomendasi anggaran dan dampaknya terhadap konsistensi menabung pengguna.
* Analisis Statistik: Menggunakan metrik terukur untuk menjawab pertanyaan bisnis terkait perubahan perilaku finansial pengguna.

### 3. [Dashboard (Streamlit)](./Dashboard)
Fokus pada penyajian informasi (Explanatory Analysis) yang dapat diakses publik:
* Interactive Analytics: Dashboard interaktif yang menampilkan kesimpulan visual dari data transaksi keuangan.
* Deployment: Aplikasi dashboard telah dideploy secara publik menggunakan Streamlit Cloud.

---

## Pertanyaan Bisnis SMART yang Dijawab
1. Rekomendasi Anggaran (Budgeting): Bagaimana fitur rekomendasi anggaran pada FinSmart membantu pengguna mengontrol pengeluaran agar tidak melebihi batas anggaran bulanan dalam satu periode?
2. Kesiapan Investasi: Bagaimana fitur analisis kesiapan investasi (berdasarkan kalkulasi otomatis Basic Liquidity Ratio & Savings Ratio) membantu pengguna mengetahui kestabilan keuangan mereka sebelum berinvestasi?
3. Machine Learning: Bagaimana algoritma Machine Learning dapat mengklasifikasikan perilaku finansial pengguna (Hemat, Normal, Boros) berdasarkan histori pengeluaran bulanan?

---

## Langkah Menjalankan Proyek Secara Lokal

1. Clone Repositori Ini:
   ```bash
   git clone [https://github.com/FinSmartTeam/data-science-FinSmart.git](https://github.com/FinSmartTeam/data-science-FinSmart.git)
   cd data-science-FinSmart
