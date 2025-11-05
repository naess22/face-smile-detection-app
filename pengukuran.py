# pengukuran.py
import streamlit as st
import pandas as pd
import numpy as np

# --- Judul dan Deskripsi ---
st.title("Sistem Pengukuran Suhu dan Kelembapan Udara")
st.subheader("Data Sensor Lingkungan")
st.write("Aplikasi ini menampilkan hasil simulasi pengukuran suhu dan kelembapan, serta visualisasi data.")

st.header("Parameter Pengukuran")
st.text("Pastikan sensor terkalibrasi dengan baik sebelum mengambil data.")
st.markdown("**Sensor DHT11/DHT22**, *Monitoring Lingkungan*, [Pelajari Lebih Lanjut](https://id.wikipedia.org/wiki/Sensor_suhu)")
st.divider()

# --- Gambar (Tetap sama) ---
st.image(
    "https://i.pinimg.com/1200x/cf/c7/e3/cfc7e35e87592eae3f8ff7146c48bbc1.jpg",
    caption="Ilustrasi Cuaca",
    width=300
)

# --- Widget dan Interaktif (Input Suhu dan Kelembapan) ---
st.header("Input Data Pengukuran")
suhu = st.slider("Masukkan Suhu (°C)", min_value=15.0, max_value=40.0, value=28.0, step=0.1)
kelembapan = st.slider("Masukkan Kelembapan (%)", min_value=30, max_value=100, value=75, step=1)
kondisi = st.selectbox("Pilih Kondisi", ["Cerah", "Berawan", "Hujan"])
setuju = st.checkbox("Data pengukuran telah tervalidasi")

if st.button("Kirim Data"):
    if setuju:
        st.success(f"Data Suhu {suhu}°C, Kelembapan {kelembapan}% berhasil direkam.")
        if suhu > 30:
            st.warning("Perhatian: Suhu cukup tinggi!")
        elif kelembapan < 50:
            st.warning("Perhatian: Kelembapan udara rendah!")
        else:
            st.info(f"Kondisi: {kondisi}")
    else:
        st.error("Anda harus memvalidasi data pengukuran sebelum mengirim.")

# --- Layout Kolom (Tetap sama) ---
st.header("Detail Hasil")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Suhu Saat Ini")
    st.metric(label="Suhu (°C)", value=f"{suhu}", delta="2.1")
with col2:
    st.subheader("Kelembapan Saat Ini")
    st.metric(label="Kelembapan (%)", value=f"{kelembapan}", delta="-1.5")

# --- Sidebar (MODIFIKASI DI SINI) ---
st.sidebar.title("Informasi Sensor")
st.sidebar.write("Menu untuk navigasi dan informasi terkait.")
menu = st.sidebar.selectbox("Pilih Informasi", ["Ringkasan Data", "Kalibrasi Sensor", "Standar Kualitas Udara"])

if menu == "Ringkasan Data":
    st.sidebar.write("Menampilkan ringkasan statistik dari data yang dikumpulkan.")
elif menu == "Kalibrasi Sensor":
    st.sidebar.write("Panduan dan status kalibrasi sensor suhu dan kelembapan.")
else:
    st.sidebar.write("Informasi tentang batas ideal suhu dan kelembapan (misalnya, SNI).")

# --- Visualisasi (Data dan Chart) ---
st.header("Visualisasi Data Historis")

# Membuat DataFrame dengan kolom Suhu, Kelembapan, dan Hasil Pengukuran
data_simulasi = pd.DataFrame({
    'Waktu': pd.to_datetime(['2025-01-01 09:00', '2025-01-01 10:00', '2025-01-01 11:00', '2025-01-01 12:00', '2025-01-01 13:00',
                             '2025-01-01 14:00', '2025-01-01 15:00', '2025-01-01 16:00', '2025-01-01 17:00', '2025-01-01 18:00']),
    'Suhu (°C)': np.random.uniform(25.0, 32.0, 10),
    'Kelembapan (%)': np.random.uniform(60, 85, 10),
})

# Menambahkan kolom Hasil Pengukuran
data_simulasi['Hasil Pengukuran'] = np.where(
    data_simulasi['Suhu (°C)'] > 30, 'Panas/Lembap',
    np.where(data_simulasi['Kelembapan (%)'] < 65, 'Nyaman/Kering', 'Nyaman/Lembap')
)

st.write("Tabel Pengukuran Suhu dan Kelembapan:")
st.dataframe(data_simulasi)

st.line_chart(data_simulasi.set_index('Waktu')[['Suhu (°C)', 'Kelembapan (%)']])
st.bar_chart(data_simulasi.set_index('Waktu')[['Suhu (°C)', 'Kelembapan (%)']])
st.area_chart(data_simulasi.set_index('Waktu')[['Suhu (°C)', 'Kelembapan (%)']])

# --- Peta (Lokasi Samarinda, Kalimantan Timur) ---
st.header("Lokasi Pengukuran")

# Koordinat Samarinda (sekitar 0.5058° S, 117.1565° E)
SAMARINDA_LAT = -0.5058
SAMARINDA_LON = 117.1565

# Membuat data untuk peta yang berpusat di Samarinda
map_data = pd.DataFrame(
    np.random.randn(10, 2) / [100, 100] + [SAMARINDA_LAT, SAMARINDA_LON],
    columns=['lat', 'lon']
)

st.write("Titik Pengukuran di Sekitar Samarinda, Kalimantan Timur:")
st.map(map_data)

st.divider()
st.caption("Dibuat untuk Tugas Sensor dan Akuisisi Data | Menggunakan Streamlit")