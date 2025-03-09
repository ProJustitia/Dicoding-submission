import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv("day.csv")
df.drop(columns=["instant"], inplace=True)
df["season"] = df["season"].astype("category")
df["weathersit"] = df["weathersit"].astype("category")


st.title("📊 Dashboard Peminjaman Sepeda")
st.write("Visualisasi data peminjaman sepeda berdasarkan faktor cuaca dan waktu.")


st.sidebar.header("Pilih Visualisasi")
option = st.sidebar.selectbox("Pilih Grafik", ["Boxplot Musim", "Histogram Peminjaman", "Heatmap Korelasi"])


if option == "Boxplot Musim":
    st.subheader("Boxplot Peminjaman Sepeda Berdasarkan Musim")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x=df["season"], y=df["cnt"], ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Peminjaman")
    st.pyplot(fig)


elif option == "Histogram Peminjaman":
    st.subheader("Histogram Distribusi Jumlah Peminjaman Sepeda")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["cnt"], bins=30, kde=True, color="skyblue", ax=ax)
    ax.set_xlabel("Jumlah Peminjaman")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig)


elif option == "Heatmap Korelasi":
    st.subheader("Heatmap Korelasi Faktor Cuaca dengan Peminjaman Sepeda")
    num = df.select_dtypes(include=["number"]).dropna()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(num.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)


st.write("Data diambil dari dataset Bike Sharing.")
