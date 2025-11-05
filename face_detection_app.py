import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Konfigurasi halaman
st.set_page_config(
    page_title="Face Detection App",
    page_icon="👤",
    layout="centered"
)

# Judul aplikasi
st.title("🎯 Deteksi Wajah dengan Haarcascade")
st.write("Upload gambar atau gunakan webcam untuk mendeteksi wajah")

# Load Haar Cascade model
@st.cache_resource
def load_cascade():
    cascade_path = "model/haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)
    return face_cascade

face_cascade = load_cascade()

# Fungsi untuk mendeteksi wajah
def detect_faces(image):
    # Konversi ke grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Deteksi wajah
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    # Gambar kotak di sekitar wajah
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(image, 'Wajah', (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    return image, len(faces)

# Pilihan input
option = st.radio(
    "Pilih sumber input:",
    ["Upload Gambar", "Webcam"]
)

if option == "Upload Gambar":
    # Upload file
    uploaded_file = st.file_uploader(
        "Pilih gambar...", 
        type=["jpg", "jpeg", "png"]
    )
    
    if uploaded_file is not None:
        # Baca gambar
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        # Tampilkan gambar asli
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Gambar Asli")
            st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), use_container_width=True)
        
        # Deteksi wajah
        result_image, num_faces = detect_faces(image.copy())
        
        with col2:
            st.subheader("Hasil Deteksi")
            st.image(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB), use_container_width=True)
        
        # Tampilkan jumlah wajah
        if num_faces > 0:
            st.success(f"✅ Terdeteksi {num_faces} wajah")
        else:
            st.warning("⚠️ Tidak ada wajah yang terdeteksi")

elif option == "Webcam":
    st.info("📷 Klik tombol di bawah untuk mengambil foto dari webcam")
    
    # Ambil foto dari webcam
    camera_photo = st.camera_input("Ambil foto")
    
    if camera_photo is not None:
        # Baca gambar dari webcam
        image = Image.open(camera_photo)
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Deteksi wajah
        result_image, num_faces = detect_faces(image.copy())
        
        # Tampilkan hasil
        st.subheader("Hasil Deteksi")
        st.image(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB), use_container_width=True)
        
        # Tampilkan jumlah wajah
        if num_faces > 0:
            st.success(f"✅ Terdeteksi {num_faces} wajah")
        else:
            st.warning("⚠️ Tidak ada wajah yang terdeteksi")

# Informasi tambahan
st.sidebar.header("ℹ️ Informasi")
st.sidebar.write("""
**Tentang Aplikasi:**
- Menggunakan Haarcascade untuk deteksi wajah
- Model: haarcascade_frontalface_default.xml
- Dapat mendeteksi multiple faces
- Support upload gambar atau webcam

**Cara Penggunaan:**
1. Pilih sumber input (Upload atau Webcam)
2. Upload gambar atau ambil foto
3. Lihat hasil deteksi wajah
""")

st.sidebar.markdown("---")
st.sidebar.write("Made with ❤️ using Streamlit")
