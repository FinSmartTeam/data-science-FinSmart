import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================================
# 1. PEMBUATAN DATASET SIMULASI (SYNTHETIC DATA)
# =====================================================================
n_users = 200  # Total 200 simulasi user
np.random.seed(42)

user_ids = np.arange(1, n_users + 1)
groups = np.random.choice(['A', 'B'], size=n_users)

# Income diset rata-rata 5-7 juta
income = np.random.normal(6000000, 1000000, n_users)

# Grup B diasumsikan lebih sukses mengontrol pengeluaran karena fitur rekomendasi
expenses_A = income * np.random.uniform(0.7, 0.95, n_users) # Boros
expenses_B = income * np.random.uniform(0.5, 0.8, n_users)  # Lebih terkontrol

# Gabungkan pengeluaran berdasarkan grup
expenses = np.where(groups == 'A', expenses_A, expenses_B)

# Sesuai formula FinSmart: Needs(60%), Wants(40%) dari total pengeluaran
needs = expenses * 0.6
wants = expenses * 0.4
savings = income - expenses

# Basic Liquidity Ratio (BLR) = Tabungan / Pengeluaran Bulanan
blr = savings / (expenses / 12) 

df_finsmart = pd.DataFrame({
    'user_id': user_ids,
    'group': groups,
    'monthly_income': income.round(0),
    'monthly_expenses': expenses.round(0),
    'needs': needs.round(0),
    'wants': wants.round(0),
    'monthly_savings': savings.round(0),
    'blr_score': blr.round(2)
})

print("Dataset Simulasi A/B Testing FinSmart Berhasil Dibuat:")
print(df_finsmart.head())
print("\n")

# Simpan ke CSV untuk dokumentasi repositori
df_finsmart.to_csv('finsmart_ab_test_data.csv', index=False)


# =====================================================================
# 2. PEMBERSIHAN DATA (ASSESSING & CLEANING DATA)
# =====================================================================
print("=== LANGKAH 2: PEMBERSIHAN DATA ===")

cols_to_numeric = ['monthly_income', 'monthly_expenses', 'monthly_savings']
for col in cols_to_numeric:
    df_finsmart[col] = pd.to_numeric(df_finsmart[col], errors='coerce')

print("Jumlah Missing Values sebelum dibersihkan:")
print(df_finsmart[cols_to_numeric].isnull().sum())
df_finsmart = df_finsmart.dropna(subset=cols_to_numeric)

# Hapus Outlier menggunakan metode IQR
Q1 = df_finsmart['monthly_expenses'].quantile(0.25)
Q3 = df_finsmart['monthly_expenses'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df_clean = df_finsmart[(df_finsmart['monthly_expenses'] >= lower_bound) & (df_finsmart['monthly_expenses'] <= upper_bound)].copy()
print(f"Data awal: {len(df_finsmart)} baris | Data setelah outlier dihapus: {len(df_clean)} baris\n")


# =====================================================================
# 3. EKSPLORASI DATA (EXPLORATORY DATA ANALYSIS / EDA)
# =====================================================================
print("=== LANGKAH 3: STATISTIK DESKRIPTIF ===")
eda_summary = df_clean.groupby('group')['monthly_expenses'].agg(['mean', 'median', 'std', 'count'])
print(eda_summary.round(0))
print("\n")


# =====================================================================
# 4. UJI ASUMSI STATISTIK (PREREQUISITE)
# =====================================================================
print("=== LANGKAH 4: UJI ASUMSI STATISTIK ===")

group_A = df_clean[df_clean['group'] == 'A']['monthly_expenses']
group_B = df_clean[df_clean['group'] == 'B']['monthly_expenses']

# Uji Normalitas (Shapiro-Wilk)
stat_A, p_norm_A = stats.shapiro(group_A)
stat_B, p_norm_B = stats.shapiro(group_B)
print(f"Uji Normalitas Grup A (p-value): {p_norm_A:.4f}")
print(f"Uji Normalitas Grup B (p-value): {p_norm_B:.4f}")

# Uji Homogenitas Varians (Levene)
stat_lev, p_levene = stats.levene(group_A, group_B)
print(f"Uji Homogenitas Varians (p-value): {p_levene:.4f}\n")


# =====================================================================
# 5 & 6. EKSEKUSI UJI HIPOTESIS & INTERPRETASI BISNIS
# =====================================================================
print("=== LANGKAH 5 & 6: UJI HIPOTESIS & KESIMPULAN BISNIS ===")

is_normal = (p_norm_A > 0.05) and (p_norm_B > 0.05)

if is_normal:
    print("Metode yang digunakan: Independent T-Test (Data Berdistribusi Normal)")
    equal_variances = True if p_levene > 0.05 else False
    stat, p_value = stats.ttest_ind(group_A, group_B, equal_var=equal_variances)
else:
    print("Metode yang digunakan: Mann-Whitney U Test (Data Tidak Berdistribusi Normal)")
    stat, p_value = stats.mannwhitneyu(group_A, group_B)

print(f"Hasil Statistik Uji: {stat:.4f}")
print(f"P-Value: {p_value:.4E}")

print("\n--- KESIMPULAN BISNIS ---")
if p_value < 0.05:
    avg_A = group_A.mean()
    avg_B = group_B.mean()
    efisiensi = ((avg_A - avg_B) / avg_A) * 100
    
    print("👉 KEPUTUSAN: H0 Ditolak, H1 Diterima (Signifikan!)")
    print(f"👉 INSIGHT: Fitur 'Rekomendasi Anggaran' pada FinSmart secara nyata membantu pengguna mengontrol keuangan mereka.")
    print(f"   Pengguna di Grup B berhasil menekan pengeluaran rata-rata bulanan sebesar {efisiensi:.1f}% lebih hemat dibanding Grup A.")
else:
    print("👉 KEPUTUSAN: Gagal Menolak H0 (Tidak Signifikan)")
    print("👉 INSIGHT: Fitur baru tidak memberikan perubahan perilaku menabung yang berarti pada pengguna website FinSmart.")


# =====================================================================
# 7. VISUALISASI UNTUK LAPORAN PDF (Explanatory Analysis)
# =====================================================================
plt.figure(figsize=(12, 5))

# Subplot 1: Boxplot
plt.subplot(1, 2, 1)
sns.boxplot(x='group', y='monthly_expenses', data=df_clean, palette='Set2')
plt.title('Perbandingan Pengeluaran: Grup A vs Grup B')
plt.ylabel('Nominal Pengeluaran Bulanan (Rp)')
plt.xlabel('Grup User')

# Subplot 2: Histogram
plt.subplot(1, 2, 2)
sns.histplot(data=df_clean, x='monthly_expenses', hue='group', kde=True, palette='Set2', multiple='dodge')
plt.title('Distribusi Sebaran Pengeluaran Bulanan')
plt.xlabel('Nominal Pengeluaran (Rp)')
plt.ylabel('Jumlah User')

plt.tight_layout()

# Menyimpan hasil grafik menjadi gambar PNG untuk dimasukkan ke laporan PDF
plt.savefig('ab_testing_finsmart_result.png', dpi=300)
print("\nGrafik visualisasi berhasil disimpan sebagai 'ab_testing_finsmart_result.png'")

# Menampilkan grafik di layar
plt.show()