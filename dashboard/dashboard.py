import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")  # Ganti dengan nama file dataset
    df["dteday"] = pd.to_datetime(df["dteday"])
    df["month"] = df["dteday"].dt.month
    df["season"] = df["season"].astype("category")
    df["weathersit"] = df["weathersit"].astype("category")
    df["weekday"] = df["weekday"].astype("category")
    return df

df = load_data()

# Judul Dashboard
st.title("Dashboard Bike Sharing 🚴")

# Sidebar untuk Filter
st.sidebar.header("Filter Data")
season_options = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
selected_season = st.sidebar.selectbox("Pilih Musim:", list(season_options.keys()), format_func=lambda x: season_options[x])
working_day = st.sidebar.checkbox("Tampilkan hanya hari kerja")

# Filter data berdasarkan pilihan
filtered_df = df[df["season"] == selected_season]
if working_day:
    filtered_df = filtered_df[filtered_df["workingday"] == 1]

# **Visualisasi 1: Distribusi Data Peminjaman Sepeda**
st.subheader("Distribusi Jumlah Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(filtered_df['cnt'], bins=30, kde=True, ax=ax)
ax.set_xlabel("Jumlah Peminjaman")
ax.set_ylabel("Frekuensi")
st.pyplot(fig)

# **Visualisasi 2: Tren Peminjaman Sepeda dalam Setahun**
st.subheader("Tren Peminjaman Sepeda dalam Kurun Waktu Setahun")
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=df.groupby("month")["cnt"].mean().reset_index(), x="month", y="cnt", marker='o', ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Peminjaman Sepeda")
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
ax.grid(True)
st.pyplot(fig)

# **Visualisasi 3: Korelasi Faktor Cuaca dengan Jumlah Peminjaman**
st.subheader("Korelasi Faktor Cuaca dengan Jumlah Peminjaman")
num_df = df.select_dtypes(include=['number'])
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(num_df.corr()[["cnt"]], annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# **Visualisasi 4: Hubungan Suhu dengan Peminjaman Sepeda di Hari Kerja**
st.subheader("Hubungan Suhu dengan Peminjaman Sepeda di Hari Kerja")
weekday_df = df[df["workingday"] == 1]
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x="temp", y="cnt", data=weekday_df, alpha=0.5, ax=ax)
ax.set_xlabel("Suhu")
ax.set_ylabel("Jumlah Peminjaman Sepeda")
st.pyplot(fig)

# **Visualisasi 5: Peminjaman Sepeda Berdasarkan Musim**
st.subheader("Peminjaman Sepeda Berdasarkan Musim")
season_counts = df.groupby("season")["cnt"].mean()
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x=season_counts.index, y=season_counts.values, ax=ax)
ax.set_xticklabels([season_options[i] for i in season_counts.index])
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Peminjaman Sepeda")
st.pyplot(fig)

st.write("Gunakan sidebar untuk memilih musim dan filter hari kerja.")

