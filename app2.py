from google import genai
from google.genai import types
from PIL import Image
import os

from dotenv import load_dotenv
import time

# Load variabel dari file .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Pastikan API_KEY terbaca
if not API_KEY:
    print("Error: API Key tidak ditemukan di file .env!")
    exit()
    
# 2. INSTRUKSI SISTEM (Diperkuat untuk Visual)
INTRUKSI_MEDIS2 = """
Anda adalah 'Antigravity Health Agent'. 
Tugas: Melakukan triase medis berdasarkan teks DAN gambar yang dikirim pasien.
Protokol Visual:
- Jika ada foto luka/gejala, analisis penampakannya (warna, bentuk, tingkat keparahan).
- JANGAN memberikan diagnosa pasti, gunakan kata 'Indikasi' atau 'Kemungkinan'.
- Tetap berikan Kategori [MERAH/KUNING/HIJAU] dan Rekomendasi Spesialis.
"""

def analisis_gejala_visual(path_gambar, pesan_teks):
    print(f"\n--- SEDANG MENGANALISIS GAMBAR DAN TEKS ---")
    
    # Membuka gambar menggunakan Pillow
    img = Image.open(path_gambar)
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[img, pesan_teks], # Kirim gambar DAN teks sekaligus!
            config=types.GenerateContentConfig(
                system_instruction=INTRUKSI_MEDIS2,
                temperature=0.3
            )
        )
        print(f"\nHasil Analisis Agen:\n{response.text}\n")
    except Exception as e:
        print(f"Error: {e}")

# TEST JALANKAN SECARA OTOMATIS
if __name__ == "__main__":
    # Pastikan file 'gejala.jpg' ada di folder yang sama
    file_gejala = "gejala.jpg"
    
    if os.path.exists(file_gejala):
        pertanyaan = "Dok, benjolan tiba tiba muncul besar di leher saya dalam sehari, kenapa ya"
        analisis_gejala_visual(file_gejala, pertanyaan)
    else:
        print(f"File {file_gejala} tidak ditemukan! Tolong taruh foto di folder proyek.")