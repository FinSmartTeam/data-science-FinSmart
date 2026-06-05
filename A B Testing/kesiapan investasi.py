import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# membuat data sintesis
n_users = 200
np.random.seed(42)

user_ids = np.arange(1, n_users + 1)
groups = np.random.choice(['A', 'B'], size=n_users)
income = np.random.normal(6000000, 500000, n_users)

# Simulasi diasumsikan Grup B lebih disiplin menabung karena melihat indikator kesiapan investasi
# Grup A menabung rata-rata 10% (SR rendah)
# Grup B menabung rata-rata 25% (SR tinggi)
savings_A = income * np.random.uniform(0.05, 0.15, n_users)
savings_B = income * np.random.uniform(0.20, 0.35, n_users)
savings = np.where(groups == 'A', savings_A, savings_B)

expenses = income - savings
total_savings_accumulated = savings * np.random.uniform(2, 8, n_users) # Total tabungan terkumpul

# Hitung Metrik Utama FinSmart
# 1. Basic Liquidity Ratio (BLR) = Total Savings / Monthly Expenses
blr = total_savings_accumulated / expenses

# 2. Savings Ratio (SR) = Monthly Savings / Monthly Income
sr = savings / income

df_finsmart = pd.DataFrame({
    'user_id': user_ids,
    'group': groups,
    'monthly_income': income.round(0),
    'monthly_expenses': expenses.round(0),
    'monthly_savings': savings.round(0),
    'savings_ratio': sr.round(4),
    'blr_score': blr.round(2)
})

# uji A/B 
print("=== ANALISIS A/B TESTING FINSMART (INVESTASI & BEHAVIOR) ===\n")

group_A_blr = df_finsmart[df_finsmart['group'] == 'A']['blr_score']
group_B_blr = df_finsmart[df_finsmart['group'] == 'B']['blr_score']

# Uji T-Test untuk BLR (Kesiapan Investasi)
stat_blr, p_blr = stats.ttest_ind(group_A_blr, group_B_blr)

print(f"Rata-rata BLR Grup A (Tanpa Fitur): {group_A_blr.mean():.2f}")
print(f"Rata-rata BLR Grup B (Dengan Fitur): {group_B_blr.mean():.2f}")
print(f"P-Value Uji BLR: {p_blr:.4E}")

print("\n--- KESIMPULAN KESIAPAN INVESTASI ---")
if p_blr < 0.05:
    print(" Fitur Kesiapan Investasi SECARA SIGNIFIKAN meningkatkan ketahanan finansial (BLR) pengguna.")
else:
    print("Tidak ada perbedaan signifikan pada kesiapan investasi.")

# plot
plt.figure(figsize=(12, 5))

# Subplot 1: Perbandingan Kesiapan Investasi (BLR)
plt.subplot(1, 2, 1)
sns.barplot(x='group', y='blr_score', data=df_finsmart, palette='Blues')
plt.axhline(y=3, color='r', linestyle='--', label='Batas Cukup Sehat (BLR=3)')
plt.title('Dampak Fitur Terhadap Kesiapan Investasi (BLR)')
plt.ylabel('Skor Basic Liquidity Ratio')
plt.legend()

# Subplot 2: Perbandingan Perilaku Menabung (Savings Ratio)
plt.subplot(1, 2, 2)
sns.boxplot(x='group', y='savings_ratio', data=df_finsmart, palette='Greens')
plt.axhline(y=0.20, color='r', linestyle='--', label='Target Ideal (20%)')
plt.title('Dampak Fitur Terhadap Perilaku Menabung (SR)')
plt.ylabel('Savings Ratio (Persentase)')
plt.legend()

plt.tight_layout()
plt.savefig('ab_test_investment_behavior.png', dpi=300)
print("\nGrafik 'ab_test_investment_behavior.png' telah disimpan.")
plt.show()
