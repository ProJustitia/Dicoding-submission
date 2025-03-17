import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")  
    df["season"] = df["season"].astype("category")
    df["weathersit"] = df["weathersit"].astype("category")
    df["dteday"] = pd.to_datetime(df["dteday"])  
    return df

df = load_data()


st.title("Dashboard Bike Sharing 🚴")


st.sidebar.header("Filter Data")
season_options = {0: "Semua Musim", 1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
selected_season = st.sidebar.multiselect("Pilih Musim:", list(season_options.keys()), format_func=lambda x: season_options[x], default=[0])
working_day = st.sidebar.checkbox("Tampilkan hanya hari kerja")


if 0 in selected_season:
    filtered_df = df
else:
    filtered_df = df[df["season"].isin(selected_season)]

if working_day:
    filtered_df = filtered_df[filtered_df["workingday"] == 1]


st.subheader("Tren Peminjaman Sepeda dalam Setahun")
fig, ax = plt.subplots(figsize=(15, 5))
sns.lineplot(x="dteday", y="cnt", data=filtered_df, ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Peminjaman Sepeda")
ax.set_title("Tren Peminjaman Sepeda Sepanjang Tahun")
st.pyplot(fig)


st.subheader("Hubungan Suhu dengan Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x="temp", y="cnt", data=filtered_df, alpha=0.5, ax=ax)
ax.set_xlabel("Suhu Normalisasi")
ax.set_ylabel("Jumlah Peminjaman Sepeda")
st.pyplot(fig)


st.subheader("Distribusi Peminjaman Sepeda Berdasarkan Musim")
season_counts = filtered_df.groupby("season")["cnt"].mean()
fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(x=season_counts.index, y=season_counts.values, ax=ax)
ax.set_xticklabels([season_options[i] for i in season_counts.index])
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Peminjaman Sepeda")
st.pyplot(fig)


st.write("Gunakan sidebar untuk memilih musim dan filter hari kerja.")

