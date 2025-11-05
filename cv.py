# cv_detection.py
import streamlit as st
import cv2
import numpy as np
import time

st.set_page_config(page_title="Computer Vision with OpenCV", layout="wide")

st.title("Deteksi Warna Berbasis HSV")
st.markdown("Gunakan **Unggah File** atau **Webcam** untuk memulai deteksi.")

# --- Bagian Input File dan Sumber ---
st.sidebar.header("Pilih Sumber Input")
input_source = st.sidebar.radio("Sumber:", ("Webcam (Real-time)", "Unggah Gambar/Video"))

uploaded_file = None
if input_source == "Unggah Gambar/Video":
    uploaded_file = st.sidebar.file_uploader(
        "Unggah Gambar (JPG, PNG) atau Video (MP4, AVI)",
        type=['jpg', 'jpeg', 'png', 'mp4', 'avi']
    )

# --- Pengaturan HSV ---
st.sidebar.header("Pengaturan HSV")
h_min = st.sidebar.slider("Hue Min", 0, 179, 0)
h_max = st.sidebar.slider("Hue Max", 0, 179, 179)
s_min = st.sidebar.slider("Saturation Min", 0, 255, 0)
s_max = st.sidebar.slider("Saturation Max", 0, 255, 255)
v_min = st.sidebar.slider("Value Min", 0, 255, 0)
v_max = st.sidebar.slider("Value Max", 0, 255, 255)

# --- Tombol Kontrol ---
if input_source == "Webcam (Real-time)":
    start_button = st.sidebar.button("Mulai Deteksi Warna")
    stop_button = st.sidebar.button("Berhenti Deteksi Warna")
else:
    # Hanya butuh satu tombol proses untuk file statis
    process_button = st.sidebar.button("Proses File Terunggah")


if "streaming" not in st.session_state:
    st.session_state.streaming = False

# Logika Tombol untuk Webcam
if input_source == "Webcam (Real-time)":
    if start_button:
        st.session_state.streaming = True
    if stop_button:
        st.session_state.streaming = False
        
# --- Placeholder dan Fungsi Deteksi ---
frame_placeholder = st.empty()

def detect_color(frame, h_min, h_max, s_min, s_max, v_min, v_max):
    """Menerapkan filter HSV pada frame yang diberikan."""
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_hsv = np.array([h_min, s_min, v_min])
    upper_hsv = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)
    result_frame = cv2.bitwise_and(frame, frame, mask=mask)
    return frame, result_frame

# --- Logika Utama: Streaming Webcam ---
if input_source == "Webcam (Real-time)" and st.session_state.streaming:
    cap = cv2.VideoCapture(0)
    time.sleep(2)  # Tunggu kamera siap

    while st.session_state.streaming:
        ret, frame = cap.read()
        if not ret:
            st.error("Gagal menangkap frame dari kamera.")
            break
        
        original, result = detect_color(frame, h_min, h_max, s_min, s_max, v_min, v_max)

        # Gabungkan dan tampilkan frame
        combined_frame = np.hstack((original, result))
        combined_frame = cv2.cvtColor(combined_frame, cv2.COLOR_BGR2RGB)
        
        # Tambahkan label
        original_label = "Original"
        result_label = "Hasil Deteksi"
        
        # Streamlit tidak mendukung penempatan label di atas gambar hstack, kita gunakan dua kolom sebagai gantinya
        col1, col2 = frame_placeholder.columns(2)
        with col1:
            st.write(original_label)
            st.image(cv2.cvtColor(original, cv2.COLOR_BGR2RGB), channels="RGB", use_column_width=True)
        with col2:
            st.write(result_label)
            st.image(cv2.cvtColor(result, cv2.COLOR_BGR2RGB), channels="RGB", use_column_width=True)


    cap.release()
    frame_placeholder.empty()
    st.session_state.streaming = False # Atur ulang status setelah selesai

# --- Logika Utama: Unggah Gambar ---
elif input_source == "Unggah Gambar/Video" and uploaded_file is not None and process_button:
    
    # Memproses Gambar
    if uploaded_file.type in ['image/jpeg', 'image/png']:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)

        original, result = detect_color(frame, h_min, h_max, s_min, s_max, v_min, v_max)
        
        # Tampilkan hasilnya menggunakan kolom
        st.subheader("Hasil Deteksi Warna pada Gambar")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Original Image")
            st.image(cv2.cvtColor(original, cv2.COLOR_BGR2RGB), channels="RGB")
        with col2:
            st.write("Result Frame (Filtered)")
            st.image(cv2.cvtColor(result, cv2.COLOR_BGR2RGB), channels="RGB")

    # Memproses Video (Sederhana)
    elif uploaded_file.type in ['video/mp4', 'video/avi']:
        st.warning("Deteksi Video sedang dikembangkan. Saat ini, hanya frame pertama yang akan diproses.")
        
        tfile = time.mkstemp()[1]
        with open(tfile, 'wb') as f:
            f.write(uploaded_file.read())
        
        cap = cv2.VideoCapture(tfile)
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            original, result = detect_color(frame, h_min, h_max, s_min, s_max, v_min, v_max)
            
            # Tampilkan hasilnya menggunakan kolom
            st.subheader("Hasil Deteksi Warna pada Frame Video (Frame Pertama)")
            col1, col2 = st.columns(2)
            with col1:
                st.write("Original Frame")
                st.image(cv2.cvtColor(original, cv2.COLOR_BGR2RGB), channels="RGB")
            with col2:
                st.write("Result Frame (Filtered)")
                st.image(cv2.cvtColor(result, cv2.COLOR_BGR2RGB), channels="RGB")

        else:
            st.error("Gagal membaca frame dari file video yang diunggah.")

# --- Pesan Default ---
elif not st.session_state.streaming and input_source == "Webcam (Real-time)":
    st.info("Tekan tombol **Mulai Deteksi Warna** di sidebar untuk mengaktifkan webcam.")
elif input_source == "Unggah Gambar/Video" and uploaded_file is None:
    st.info("Unggah file gambar atau video dan tekan **Proses File Terunggah**.")