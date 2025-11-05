import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Konfigurasi halaman
st.set_page_config(
    page_title="Face & Smile Detection App",
    page_icon="😊",
    layout="centered"
)

# Judul aplikasi
st.title("😁 Deteksi Wajah dan Senyum dengan Haarcascade")
st.write("Upload gambar atau gunakan webcam untuk mendeteksi wajah dan senyum")

# Load Haar Cascade models
@st.cache_resource
def load_cascades():
    # Asumsikan file ini ada di lokasi yang sama atau yang ditentukan
    face_cascade_path = "model/haarcascade_frontalface_default.xml" 
    smile_cascade_path = "model/haarcascade_smile.xml" # ASUMSI: File smile cascade ada

    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    smile_cascade = cv2.CascadeClassifier(smile_cascade_path)
    
    # Cek apakah model berhasil dimuat
    if face_cascade.empty() or smile_cascade.empty():
        st.error("Gagal memuat salah satu atau kedua model cascade. Pastikan file 'haarcascade_frontalface_default.xml' dan 'haarcascade_smile.xml' ada di folder 'model/'.")
        return None, None
        
    return face_cascade, smile_cascade

face_cascade, smile_cascade = load_cascades()

# Hanya jalankan aplikasi jika model berhasil dimuat
if face_cascade is not None and smile_cascade is not None:
    # Fungsi untuk mendeteksi wajah dan senyum
    def detect_faces_and_smiles(image):
        # Konversi ke grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Deteksi wajah (Menggunakan skala yang sama dengan sebelumnya)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        num_smiles = 0
        
        # Gambar kotak di sekitar wajah
        for (x, y, w, h) in faces:
            # Gambar kotak wajah (Warna Hijau)
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(image, 'Wajah', (x, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            # **Deteksi Senyum di dalam Area Wajah**
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
            
            smiles = smile_cascade.detectMultiScale(
                roi_gray,
                scaleFactor=1.7,  # Senyum lebih sensitif, gunakan scaleFactor dan minNeighbors yang berbeda
                minNeighbors=22,
                minSize=(25, 25)
            )
            
            # Gambar kotak senyum
            for (sx, sy, sw, sh) in smiles:
                # Gambar kotak senyum (Warna Biru)
                cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (255, 0, 0), 2)
                cv2.putText(roi_color, 'Senyum!', (sx, sy+sh+20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                num_smiles += 1
        
        return image, len(faces), num_smiles

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
            
            # Deteksi wajah dan senyum
            result_image, num_faces, num_smiles = detect_faces_and_smiles(image.copy())
            
            with col2:
                st.subheader("Hasil Deteksi")
                st.image(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB), use_container_width=True)
            
            # Tampilkan jumlah hasil
            if num_faces > 0:
                st.success(f"✅ Terdeteksi **{num_faces}** wajah")
            else:
                st.warning("⚠️ Tidak ada wajah yang terdeteksi")
                
            if num_smiles > 0:
                st.info(f"😊 Terdeteksi **{num_smiles}** senyum")
            else:
                st.info("😐 Tidak ada senyum yang terdeteksi")

    elif option == "Webcam":
        st.info("📷 Klik tombol di bawah untuk mengambil foto dari webcam")
        
        # Ambil foto dari webcam
        camera_photo = st.camera_input("Ambil foto")
        
        if camera_photo is not None:
            # Baca gambar dari webcam
            image = Image.open(camera_photo)
            image = np.array(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Deteksi wajah dan senyum
            result_image, num_faces, num_smiles = detect_faces_and_smiles(image.copy())
            
            # Tampilkan hasil
            st.subheader("Hasil Deteksi")
            st.image(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB), use_container_width=True)
            
            # Tampilkan jumlah hasil
            if num_faces > 0:
                st.success(f"✅ Terdeteksi **{num_faces}** wajah")
            else:
                st.warning("⚠️ Tidak ada wajah yang terdeteksi")
                
            if num_smiles > 0:
                st.info(f"😊 Terdeteksi **{num_smiles}** senyum")
            else:
                st.info("😐 Tidak ada senyum yang terdeteksi")

    # Informasi tambahan
    st.sidebar.header("ℹ️ Informasi")
    st.sidebar.write("""
    **Tentang Aplikasi:**
    - Menggunakan **Haarcascade** untuk deteksi wajah dan senyum
    - Model: `haarcascade_frontalface_default.xml` & `haarcascade_smile.xml`
    - Deteksi senyum dilakukan **di dalam** area wajah yang terdeteksi.
    - Support upload gambar atau webcam

    **Cara Penggunaan:**
    1. Pilih sumber input (Upload atau Webcam)
    2. Upload gambar atau ambil foto
    3. Lihat hasil deteksi wajah (kotak hijau) dan senyum (kotak biru)
    """)

    st.sidebar.markdown("---")
    st.sidebar.write("Made with ❤️ using Streamlit")