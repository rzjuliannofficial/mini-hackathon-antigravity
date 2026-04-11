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

# 2. DEFINISI INSTRUKSI AGEN (System Instruction)
# Ini adalah "kepribadian" dan "protokol" AI kamu.
INTRUKSI_MEDIS1 = """
Anda adalah 'Health Agent'. Tugas Anda adalah melakukan triase pasien secara cepat.
Aturan main:
1. Analisis keluhan pasien (teks/gambar).
2. Tentukan kategori: 
   - MERAH (Gawat Darurat - Segera ke UGD)
   - KUNING (Perlu penanganan medis segera tapi stabil)
   - HIJAU (Gejala ringan - Rawat jalan/Puskesmas)
3. Berikan saran departemen spesialis yang tepat.
4. Gunakan gaya bicara yang profesional, empati, namun sangat ringkas.
5. Jika ada indikasi ancaman nyawa, berikan peringatan keras di awal jawaban.
"""

def jalankan_triase():
    print("--- HEALTH AGENT AKTIF ---")
    print("Ketik 'keluar' untuk berhenti.\n")
    
    while True:
        user_input = input("Pasien: ")
        if user_input.lower() == 'keluar':
            break
            
        try:
            # Menggunakan model gemini-2.5-flash yang tersedia
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=INTRUKSI_MEDIS1,
                    temperature=0.7 # Biar jawaban lebih natural
                )
            )
            
            print(f"\nAgen AI: \n{response.text}\n")
            print("-" * 30)
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    jalankan_triase()