import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")  # Ganti dengan nama file dataset
    df["season"] = df["season"].astype("category")
    df["weathersit"] = df["weathersit"].astype("category")
    return df

df = load_data()

# Judul Dashboard
st.title("Dashboard Bike Sharing 🚴")

# Sidebar untuk Filter
st.sidebar.header("Filter Data")
season_options = {0: "Semua Musim", 1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
selected_season = st.sidebar.multiselect("Pilih Musim:", list(season_options.keys()), format_func=lambda x: season_options[x], default=[0])
working_day = st.sidebar.checkbox("Tampilkan hanya hari kerja")

# Filter data berdasarkan pilihan musim
if 0 in selected_season:  # Jika "Semua Musim" dipilih, tampilkan semua data
    filtered_df = df
else:
    filtered_df = df[df["season"].isin(selected_season)]

if working_day:
    filtered_df = filtered_df[filtered_df["workingday"] == 1]

# **Visualisasi 1: Scatter Plot Hubungan Suhu dan Peminjaman**
st.subheader("Hubungan Suhu dengan Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x="temp", y="cnt", data=filtered_df, alpha=0.5, ax=ax)
ax.set_xlabel("Suhu Normalisasi")
ax.set_ylabel("Jumlah Peminjaman Sepeda")
st.pyplot(fig)

# **Visualisasi 2: Bar Plot Peminjaman Sepeda Berdasarkan Musim**
st.subheader("Distribusi Peminjaman Sepeda Berdasarkan Musim")
season_counts = df.groupby("season")["cnt"].mean()
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x=season_counts.index, y=season_counts.values, ax=ax)
ax.set_xticklabels([season_options[i] for i in season_counts.index])
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Peminjaman Sepeda")
st.pyplot(fig)

# Tambahan informasi
st.write("Gunakan sidebar untuk memilih musim dan filter hari kerja.")

