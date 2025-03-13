import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.header('Analisis Perilaku Customer Dalam Penyewaan Sepeda  :sparkles:')
st.subheader('Analisis penyewaan Perkondisi')

# Membaca dataset
url1 = "https://raw.githubusercontent.com/DananRukmana/DananRukmana/refs/heads/main/hour.csv"
url2 = "https://raw.githubusercontent.com/DananRukmana/DananRukmana/refs/heads/main/day.csv"
df1 = pd.read_csv(url1)
df_hour = pd.DataFrame(df1)
df2 = pd.read_csv(url2)
df_day = pd.DataFrame(df2)

# Visualisasi 1: Tren Penyewaan Sepeda per Jam
jam_sibuk = df_hour.groupby('hr')['cnt'].sum()
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(jam_sibuk.index, jam_sibuk.values, marker='o', linestyle='-', color='g')
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Rata-rata Jumlah Penyewaan sepeda')
ax.set_title('Tren Penyewaan Sepeda per Jam')
ax.set_xticks(range(0, 24))
ax.grid()
st.pyplot(fig)

st.subheader("Analisis Kondisi Saat Customer Melakukan Penyewaan")

# Fungsi untuk mengelompokkan waktu
def kelompok_waktu(jam):
    if 0 <= jam < 6:
        return "Malam (00:00-05:59)"
    elif 6 <= jam < 12:
        return "Pagi (06:00-11:59)"
    elif 12 <= jam < 18:
        return "Siang (12:00-17:59)"
    else:
        return "Sore (18:00-23:59)"

df_hour["kategori_waktu"] = df_hour["hr"].apply(kelompok_waktu)

# Sidebar
with st.sidebar:
    st.header('Dashboard Penyewaan Sepeda 🚴')

    
    weather_labels = {
        1: "Cerah",
        2: "Berawan",
        3: "Hujan / Salju Ringan"
    }

    selected_weather = st.selectbox("🌦️ Pilih Kondisi Cuaca", list(weather_labels.values()))

    
    cuaca = df_day.groupby('weathersit')['cnt'].sum()
    cuaca.index = cuaca.index.map(weather_labels)

    
    if "show_percentage" not in st.session_state:
        st.session_state["show_percentage"] = False

    if st.button("Cek Persentase 📊"):
        st.session_state["show_percentage"] = True

    if st.session_state["show_percentage"]:
        percentage = (cuaca[selected_weather] / cuaca.sum()) * 100
        st.metric(label=f"Persentase Penyewaan Saat **{selected_weather}**", value=f"{percentage:.1f}%")


cuaca = df_day.groupby('weathersit').cnt.sum()
cuaca.index = cuaca.index.map(weather_labels)
colors = ["green", "gold", "blue"]  
explode = [0.5 if (w == selected_weather and st.session_state["show_percentage"] and cuaca[w] / cuaca.sum() < 0.05) else
           0.3 if (w == selected_weather and st.session_state["show_percentage"]) else
           0 for w in cuaca.index]



fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(
    cuaca.values, labels=cuaca.index, autopct='%1.1f%%',
    colors=colors, startangle=140, explode=explode,
    wedgeprops={'edgecolor': 'black', 'linewidth': 1.5}
)
ax.set_title("Pengaruh Cuaca terhadap Penyewaan Sepeda", fontsize=14, fontweight='bold')
ax.legend(title="Kondisi Cuaca", loc="best", fontsize=10)
st.pyplot(fig)

st.subheader("Analisis Kondisi Pola Penyewaan Kelompok jam")


df_hour["kategori_waktu"] = df_hour["hr"].apply(kelompok_waktu)
waktu_digunakan = df_hour.groupby("kategori_waktu")["cnt"].sum()
fig, ax = plt.subplots(figsize=(8, 5))
colors = ["blue", "orange", "green", "red"]  
sns.barplot(x=waktu_digunakan.index, y=waktu_digunakan.values, palette=colors, ax=ax)
ax.set_xlabel("Kategori Waktu")
ax.set_ylabel("Total Peminjaman Sepeda")
ax.set_title("Peminjaman Sepeda Berdasarkan Waktu Penggunaan")
ax.set_xticks(range(len(waktu_digunakan)))
ax.set_xticklabels(waktu_digunakan.index, rotation=30)
st.pyplot(fig)

st.caption('Danan Rukmana / 08 04 2025')
