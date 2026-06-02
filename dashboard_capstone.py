import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

st.set_page_config(
    page_title="Student Expense Dashboard",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("dataset_mahasiswa_realistis.csv")

df = load_data()

# =========================
# FILTER HANYA PENGELUARAN
# =========================
expense_df = df[df["TransactionType"] == "Expenses"]

# =========================
# SIDEBAR
# =========================
st.sidebar.header("Filter Bulan")

available_months = sorted(expense_df["Month"].unique())

selected_months = st.sidebar.multiselect(
    "Pilih Bulan",
    available_months,
    default=available_months
)

# =========================
# TITLE
# =========================
st.title("📊 Distribusi Pengeluaran per Kategori")

# =========================
# PIE CHART
# =========================

st.header("1. Distribusi Pengeluaran per Kategori (Pie Chart)")

for row_start in range(0, len(selected_months), 3):

    cols = st.columns(3)

    for col_idx, month in enumerate(
        selected_months[row_start:row_start+3]
    ):

        with cols[col_idx]:

            month_data = expense_df[
                expense_df["Month"] == month
            ]

            category_expense = (
                month_data
                .groupby("TransactionCategory")["Amount"]
                .sum()
                .sort_values(ascending=False)
            )

            total_expense = category_expense.sum()

            fig, ax = plt.subplots(figsize=(5,5))

            ax.pie(
                category_expense,
                labels=category_expense.index,
                autopct="%1.1f%%",
                startangle=90
            )

            ax.set_title(
                f"Periode: {month}\nTotal: Rp {total_expense:,.0f}"
            )

            st.pyplot(fig)

# =========================
# INSIGHT
# =========================
st.markdown("---")
st.subheader("📝 Insight")

insights = []

for month in selected_months:

    month_data = expense_df[
        expense_df["Month"] == month
    ]

    category_expense = (
        month_data
        .groupby("TransactionCategory")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    largest_category = category_expense.idxmax()

    percentage = (
        category_expense.max()
        / category_expense.sum()
        * 100
    )

    insights.append(
        f"Pada bulan **{month}**, kategori pengeluaran terbesar adalah **{largest_category}** dengan proporsi sekitar **{percentage:.1f}%** dari total pengeluaran."
    )

for text in insights:
    st.write("•", text)

# =========================
# 2. MONTHLY EXPENSES TREND
# =========================

st.divider()

st.header("2. Monthly Expenses Trend (Line Chart)")

months = sorted(expense_df["Month"].unique())

col1, col2 = st.columns(2)

with col1:
    start_month = st.selectbox(
        "Pilih Bulan Awal",
        months,
        index=0
    )

with col2:
    end_month = st.selectbox(
        "Pilih Bulan Akhir",
        months,
        index=len(months)-1
    )

# Validasi range
start_idx = months.index(start_month)
end_idx = months.index(end_month)

if start_idx > end_idx:
    st.error("Bulan awal harus lebih kecil atau sama dengan bulan akhir.")
else:

    selected_months = months[start_idx:end_idx+1]

    monthly_expense = (
        expense_df[
            expense_df["Month"].isin(selected_months)
        ]
        .groupby("Month")["Amount"]
        .sum()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(
        monthly_expense["Month"],
        monthly_expense["Amount"],
        marker="o",
        linewidth=2
    )

    ax.set_title(
        f"Monthly Expenses Trend\nPeriode: {start_month} sampai {end_month}"
    )

    ax.set_xlabel("Bulan (Month)")
    ax.set_ylabel("Total Pengeluaran (Rupiah)")
    ax.grid(True)

    st.pyplot(fig)

    st.markdown("### Data Angka Tren Aktif")

    for _, row in monthly_expense.iterrows():
        st.write(
            f"- Bulan {row['Month']}: Rp {row['Amount']:,.0f}"
        )

    highest_month = monthly_expense.loc[
        monthly_expense["Amount"].idxmax()
    ]

    lowest_month = monthly_expense.loc[
        monthly_expense["Amount"].idxmin()
    ]

    st.markdown("### Insight")

    st.write(
        f"""
Berdasarkan grafik, diperoleh informasi mengenai naik turunnya total uang yang dikeluarkan mahasiswa selama periode **{start_month} hingga {end_month}**.

Pengeluaran tertinggi terjadi pada bulan **{highest_month['Month']}** sebesar **Rp {highest_month['Amount']:,.0f}**, sedangkan pengeluaran terendah terjadi pada bulan **{lowest_month['Month']}** sebesar **Rp {lowest_month['Amount']:,.0f}**.

Grafik menunjukkan adanya perubahan pola pengeluaran dari bulan ke bulan. Kenaikan pengeluaran mengindikasikan peningkatan aktivitas konsumsi pada periode tertentu, sedangkan penurunan pengeluaran menunjukkan adanya upaya penghematan atau berkurangnya kebutuhan belanja pada periode tersebut.
        """
    )

# =========================
# 3. TOP SPENDING TRANSACTIONS
# =========================

st.divider()

st.header("3. Top Spending Transactions (Table)")

col1, col2 = st.columns(2)

with col1:
    top_month = st.selectbox(
        "Pilih Bulan",
        sorted(expense_df["Month"].unique()),
        key="top_spending_month"
    )

with col2:
    top_n = st.selectbox(
        "Tampilkan Top",
        list(range(1, 11)),
        index=9
    )

# =========================
# FILTER DATA
# =========================

top_spending = (
    expense_df[
        expense_df["Month"] == top_month
    ]
    .sort_values(
        by="Amount",
        ascending=False
    )
    .head(top_n)
)

# =========================
# TABEL
# =========================

display_table = top_spending[
    [
        "Date",
        "Description",
        "TransactionCategory",
        "Amount"
    ]
].copy()

display_table["Amount"] = display_table["Amount"].apply(
    lambda x: f"Rp {x:,.0f}"
)

st.dataframe(
    display_table,
    use_container_width=True
)

# =========================
# INSIGHT
# =========================

st.subheader("📝 Insight")

highest_transaction = top_spending.iloc[0]

highest_amount = highest_transaction["Amount"]
highest_category = highest_transaction["TransactionCategory"]
highest_desc = highest_transaction["Description"]

dominant_category = (
    top_spending["TransactionCategory"]
    .value_counts()
    .idxmax()
)

dominant_count = (
    top_spending["TransactionCategory"]
    .value_counts()
    .max()
)

avg_transaction = top_spending["Amount"].mean()

st.write(
    f"""
Berdasarkan daftar **Top {top_n} Spending Transactions** pada bulan **{top_month}**, transaksi terbesar berasal dari kategori **{highest_category}** dengan nominal **Rp {highest_amount:,.0f}** untuk transaksi **{highest_desc}**.

Kategori yang paling sering muncul dalam daftar Top {top_n} adalah **{dominant_category}** sebanyak **{dominant_count} kali**, yang menunjukkan bahwa kategori tersebut memberikan kontribusi besar terhadap pengeluaran pada bulan tersebut.

Rata-rata nilai transaksi pada daftar Top {top_n} adalah sekitar **Rp {avg_transaction:,.0f}** per transaksi.

Melalui daftar transaksi terbesar ini, pengguna dapat mengidentifikasi aktivitas pengeluaran yang paling banyak menyerap anggaran serta mengetahui kategori yang paling berpengaruh terhadap total pengeluaran pada periode yang dipilih.
"""
)

# =========================
# 4. INCOME VS EXPENSES
# =========================

st.divider()

st.header("4. Income vs Expenses Comparison")

months = sorted(df["Month"].unique())

col1, col2, col3 = st.columns(3)

with col1:
    start_month_bar = st.selectbox(
        "Bulan Awal",
        months,
        index=0,
        key="income_expense_start"
    )

with col2:
    end_month_bar = st.selectbox(
        "Bulan Akhir",
        months,
        index=len(months)-1,
        key="income_expense_end"
    )

with col3:
    display_option = st.selectbox(
        "Tampilkan Data",
        [
            "Income & Expenses",
            "Income Only",
            "Expenses Only"
        ]
    )

start_idx = months.index(start_month_bar)
end_idx = months.index(end_month_bar)

if start_idx > end_idx:

    st.error(
        "Bulan awal harus lebih kecil atau sama dengan bulan akhir."
    )

else:

    selected_months_bar = months[
        start_idx:end_idx+1
    ]

    filtered_df = df[
        df["Month"].isin(selected_months_bar)
    ]

    income_monthly = (
        filtered_df[
            filtered_df["TransactionType"] == "Income"
        ]
        .groupby("Month")["Amount"]
        .sum()
    )

    expense_monthly = (
        filtered_df[
            filtered_df["TransactionType"] == "Expenses"
        ]
        .groupby("Month")["Amount"]
        .sum()
    )

    comparison_df = pd.DataFrame({
        "Income": income_monthly,
        "Expenses": expense_monthly
    }).fillna(0)

    fig, ax = plt.subplots(figsize=(10,5))

    x = range(len(comparison_df))

    width = 0.35

    if display_option == "Income & Expenses":

        ax.bar(
            [i - width/2 for i in x],
            comparison_df["Income"],
            width,
            label="Income"
        )

        ax.bar(
            [i + width/2 for i in x],
            comparison_df["Expenses"],
            width,
            label="Expenses"
        )

    elif display_option == "Income Only":

        ax.bar(
            x,
            comparison_df["Income"],
            width=0.5,
            label="Income"
        )

    else:

        ax.bar(
            x,
            comparison_df["Expenses"],
            width=0.5,
            label="Expenses"
        )

    ax.set_xticks(list(x))
    ax.set_xticklabels(comparison_df.index)

    ax.set_title(
        f"Perbandingan Income vs Expenses\nPeriode: {start_month_bar} sampai {end_month_bar}"
    )

    ax.set_xlabel("Bulan")
    ax.set_ylabel("Total Nominal (Rupiah)")

    ax.yaxis.set_major_formatter(
        FuncFormatter(
            lambda y, pos: f"Rp {y:,.0f}"
        )
    )

    ax.legend()

    st.pyplot(fig)

    st.subheader("📝 Insight")

    highest_expense_month = comparison_df[
        "Expenses"
    ].idxmax()

    highest_expense_value = comparison_df[
        "Expenses"
    ].max()

    highest_income_month = comparison_df[
        "Income"
    ].idxmax()

    highest_income_value = comparison_df[
        "Income"
    ].max()

    surplus_months = (
        comparison_df["Income"]
        > comparison_df["Expenses"]
    ).sum()

    deficit_months = (
        comparison_df["Expenses"]
        > comparison_df["Income"]
    ).sum()

    st.write(
        f"""
Pada periode **{start_month_bar} hingga {end_month_bar}**, pengeluaran terbesar terjadi pada bulan **{highest_expense_month}** sebesar **Rp {highest_expense_value:,.0f}**.

Sementara itu pemasukan selalu stabil berada di **Rp {highest_income_value:,.0f}**.

Selama periode yang dipilih terdapat **{surplus_months} bulan** dengan kondisi surplus (income lebih besar daripada expenses) dan **{deficit_months} bulan** dengan kondisi defisit (expenses lebih besar daripada income).

Grafik ini membantu melihat apakah kondisi keuangan mahasiswa berada dalam kondisi sehat, seimbang, atau mengalami pemborosan pada bulan-bulan tertentu.
"""
    )