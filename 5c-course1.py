import streamlit as st

#Judul dan Deskripsi
st.title("Mobile Legend")
st.subheader("aku adalah diggie dan diggie adalah aku")
st.write("get ixiaaa")

st.header("Draft Pick")
st.text("jangan lupa ngeban njr")
st.markdown("**Land of Dawn**, *Pick your hero*, [ban](https://ml.co.id)")
st.divider()
st.image(
    "https://i.pinimg.com/736x/d7/d6/cb/d7d6cbe90aa9445a4388b39ec877b639.jpg",
    caption="fox",
    width=250
)

st.header("Widget dan Interaktif")
nama = st.text_input("Masukkan Nama Anda")
nim = st.text_input("Masukkan NIM Anda")
prodi = st.selectbox("Pilih Prodi Anda", ["TI", "TK", "TRK", "TIM"])
setuju = st.checkbox("Saya setuju dengan syarat dan ketentuan yang berlaku")
if st.button("kirim"):
    if setuju:
        st.success(f"Terima kasih {nama} dari prodi {prodi}, data telah kami terima.")
    else:
        st.error("Anda harus menyetujui syarat dan ketentuan sebelum mengirim data.")

st.header("Sidebar")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Kolom 1")
    st.write("Ini adalah kolom pertama.")
with col2:
    st.subheader("Kolom 2")
    st.write("Ini adalah kolom kedua.")

st.sidebar.title("Sidebar")
st.sidebar.write("Ini adalah sidebar aplikasi.")
menu = st.sidebar.selectbox("Pilih Menu", ["Home", "Profil", "Contact"])
if menu == "Home":
    st.sidebar.write("Selamat datang di halaman Home.")
elif menu == "Profil":
    st.sidebar.write("Ini adalah halaman Profil.")
else:
    st.sidebar.write("Hubungi kami di halaman Contact.")

st.header("Visualisasi")
import pandas as pd
import numpy as np

data = pd.DataFrame(
    np.random.randn(10, 3),
    columns=['A', 'B', 'C']
)

st.write("Data Acak:")
st.dataframe(data)
st.line_chart(data)
st.bar_chart(data)
st.area_chart(data)
st.map(pd.DataFrame(
    np.random.randn(100, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon']
))

st.divider()
st.caption("Dibuat dengan sepenuh hati menggunakan streamlit")