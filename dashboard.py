import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

st.header('Analisis Perilaku Customer Dalam Penyewaan Sepeda :sparkles:')
# Membaca dataset
url1 = "https://raw.githubusercontent.com/DananRukmana/DananRukmana/refs/heads/main/hour.csv"
url2 = "https://raw.githubusercontent.com/DananRukmana/DananRukmana/refs/heads/main/day.csv"
df_hour = pd.read_csv(url1)
df_day = pd.read_csv(url2)

def create_byhour_df(df):
    byhour_df = df.groupby(by="hr")["cnt"].sum().reset_index()
    byhour_df.rename(columns={
        "cnt": "total_penyewa"
    }, inplace=True)
    
    return byhour_df

def create_byweather_df(df):
    byweather_df = df.groupby(by="weathersit")["cnt"].sum().reset_index()
    byweather_df.rename(columns={
        "cnt": "total_penyewa"
    }, inplace=True)
    
    return byweather_df

df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])
df_day['dteday'] = pd.to_datetime(df_day['dteday'])

min_date = df_hour["dteday"].min()
max_date = df_hour["dteday"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df_hour[(df_hour["dteday"] >= str(start_date)) & 
                  (df_hour["dteday"] <= str(end_date))]
main_df_day = df_day[(df_day["dteday"] >= str(start_date)) & 
                     (df_day["dteday"] <= str(end_date))]

byhour_df = create_byhour_df(main_df)
byweather_df = create_byweather_df(main_df_day)

st.header('Analisis perilaku penyewa sepeda :sparkles:')

st.subheader('Daily Penyewa per Jam')

col1, col2 = st.columns(2)

if not byhour_df.empty:
    max_penyewa_idx = byhour_df["total_penyewa"].idxmax()
    jam_terbanyak = byhour_df.loc[max_penyewa_idx, "hr"]
    total_penyewa = byhour_df.loc[max_penyewa_idx, "total_penyewa"]
    
    with col1:
        st.metric("Jam Paling Padat Penyewa", value=jam_terbanyak)
    
    with col2:
        st.metric("Total Penyewa", value=total_penyewa)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(byhour_df["hr"], byhour_df["total_penyewa"], marker='o', linestyle='-', color='g')
    ax.set_xlabel('Jam dalam Sehari')
    ax.set_ylabel('Total Jumlah Penyewaan Sepeda')
    ax.set_xticks(range(24))
    ax.set_title('Tren Penyewaan Sepeda per Jam')
    ax.grid()
    st.pyplot(fig)
else:
    st.warning("Tidak ada data untuk rentang waktu yang dipilih.")

# Analisis Pengaruh Cuaca
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")
cuaca = byweather_df
weather_labels = {
    1: "Cerah",
    2: "Berawan",
    3: "Hujan / Salju Ringan"
}
cuaca["weathersit"] = cuaca["weathersit"].map(weather_labels)

col1, col2, col3 = st.columns(3)
if not cuaca.empty:
    cerah_penyewa = cuaca.loc[cuaca["weathersit"] == "Cerah", "total_penyewa"].sum()
    berawan_penyewa = cuaca.loc[cuaca["weathersit"] == "Berawan", "total_penyewa"].sum()
    hujan_penyewa = cuaca.loc[cuaca["weathersit"] == "Hujan / Salju Ringan", "total_penyewa"].sum()
    
    with col1:
        st.metric("Penyewa saat Cuaca Cerah", value=cerah_penyewa)
    with col2:
        st.metric("Penyewa saat Cuaca Berawan", value=berawan_penyewa)
    with col3:
        st.metric("Penyewa saat Hujan / Salju Ringan", value=hujan_penyewa)

    fig, ax = plt.subplots(figsize=(8, 8))
    colors = ["green", "gold", "blue"]
    explode = [0.1] * len(cuaca["total_penyewa"]) 
    ax.pie(
        cuaca["total_penyewa"].values, labels=cuaca["weathersit"], autopct='%1.1f%%', 
        colors=colors, startangle=140, explode=explode, 
        wedgeprops={'edgecolor': 'black', 'linewidth': 1.5}
    )
    ax.set_title("Pengaruh Cuaca terhadap Penyewaan Sepeda", fontsize=14, fontweight='bold')
    st.pyplot(fig)
else:
    st.warning("Tidak ada data untuk rentang waktu yang dipilih.")
