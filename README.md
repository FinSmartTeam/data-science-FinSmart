## 👥 Peran & Kontribusi Spesifik (Data Science)

Dalam proyek pengembangan **FinSmart** ini, saya bertanggung jawab penuh sebagai **Data Scientist** untuk mengawal siklus pengelolaan dan analisis data dari hulu ke hilir (*end-to-end data lifecycle*). Berikut adalah rincian kontribusi konkret yang saya lakukan:

### 1. Problem Discovery & Solution Definition
* **Analisis Permasalahan:** Mengumpulkan serta memetakan berbagai isu krusial seputar perilaku finansial masyarakat Indonesia (seperti pola konsumsi berlebih vs tingkat tabungan rendah).
* **Penentuan Solusi Utama:** Merumuskan solusi utama berupa sistem penasihat keuangan pintar (*smart financial advisor*) berbasis data untuk membantu pengguna mengoptimalkan alokasi pendapatan mereka.
* **Dokumentasi Teknis:** Menyusun laporan teknis komprehensif berformat **PDF** yang mencakup seluruh perjalanan proyek, mulai dari tahap *Problem Discovery*, metodologi analisis, hingga kesimpulan akhir.

### 2. End-to-End Data Wrangling
* **Gathering Data:** Melakukan pencarian dan pengumpulan dataset publik yang relevan, memanfaatkan data perilaku keuangan Indonesia (*Indonesian Personal Finance Dataset* dari Kaggle).
* **Assessing Data:** Mengevaluasi kualitas data, memeriksa inkonsistensi struktur, serta mengidentifikasi sebaran nilai pada fitur pendapatan dan 12+ kategori pengeluaran (seperti Bahan Pokok, Tempat Tinggal, Sandang, hingga Pengeluaran Tidak Esensial).
* **Cleaning Data:** Melakukan pembersihan data (*data cleaning*) secara menyeluruh, menangani nilai kosong atau anomali agar siap diproses pada tahap analitik berikutnya.
* **Data Dictionary:** Menyusun kamus data (*Data Dictionary*) terstruktur guna mendefinisikan arti, tipe data, dan satuan dari setiap variabel keuangan demi menjaga konsistensi tim.

### 3. Exploratory & Explanatory Data Analysis (EDA)
* **Formulasi Pertanyaan Bisnis:** Mendefinisikan pertanyaan bisnis yang terukur, seperti *"Bagaimana loyalitas alokasi tabungan berbanding lurus dengan pendapatan?"* atau *"Kategori pengeluaran apa yang paling memicu perilaku boros?"*
* **Insight Discovery:** Melakukan EDA mendalam untuk mengungkap korelasi antartipe perilaku keuangan (*hemat, normal, boros*) terhadap pola alokasi dana riil.
* **Visualisasi Data:** Membuat grafik analitis interaktif dan *explanatory plots* menggunakan `matplotlib` dan `seaborn` untuk menyajikan jawaban atas pertanyaan bisnis secara visual dan intuitif.

### 4. Feature Engineering & Experimentation
* **Fitur Informatif:** Mentransformasi data mentah dan melakukan *feature engineering* untuk mengekstrak indikator finansial baru (seperti kalkulasi total pengeluaran agregat, persentase pengeluaran kebutuhan/*needs*, keinginan/*wants*, dan rasio tabungan/*savings*).
* **Kesiapan Model:** Memastikan representasi fitur sudah optimal, ternormalisasi, dan memiliki daya pemisah (*predictive power*) yang kuat sebelum dikonsumsi oleh model Machine Learning.
* **A/B Testing:** Mengimplementasikan pengujian hipotesis (A/B Testing) menggunakan Python untuk mengevaluasi efektivitas perbedaan perlakuan atau fitur finansial tertentu terhadap perubahan perilaku keuangan pengguna secara statistik.

### 5. Interactive Dashboard Development & Deployment
* **Pembangunan Dashboard:** Mengembangkan aplikasi web *dashboard* interaktif berbasis **Streamlit** untuk memvisualisasikan seluruh *insight* utama, metrik keuangan, serta ringkasan kesimpulan analisis data secara dinamis.
* **Cloud Deployment:** Melakukan *deployment* aplikasi *dashboard* tersebut ke **Streamlit Cloud** agar dapat diakses secara publik oleh para pemangku kepentingan (*stakeholders*) dan pengguna umum.
