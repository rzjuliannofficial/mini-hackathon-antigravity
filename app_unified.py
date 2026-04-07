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

client = genai.Client(api_key=API_KEY)
# 2. INSTRUKSI SISTEM GABUNGAN
INSTRUKSI_MEDIS_UNIFIED = """
Anda adalah 'Antigravity Health Agent' - Agen triase medis terpadu.

TUGAS UTAMA: Melakukan triase pasien berdasarkan INPUT:
- Teks saja (pertanyaan gejala)
- Gambar saja (foto luka/gejala)
- ATAU Gambar + Teks (kombinasi)

PROTOKOL TRIASE:
1. Analisis keluhan/gejala pasien.
2. Jika ada FOTO luka/gejala:
   - Analisis penampakannya (warna, bentuk, ukuran, tingkat keparahan)
   - Jangan berikan diagnosa pasti, gunakan "Indikasi" atau "Kemungkinan"
3. Tentukan Kategori Prioritas:
   - 🔴 MERAH (Gawat Darurat - Segera ke UGD)
   - 🟡 KUNING (Perlu penanganan medis segera tapi stabil)
   - 🟢 HIJAU (Gejala ringan - Rawat jalan/Puskesmas)
4. Berikan rekomendasi departemen/spesialis yang tepat.
5. Gunakan gaya bicara: PROFESIONAL + EMPATI + RINGKAS
6. Jika ada indikasi ancaman nyawa, berikan PERINGATAN KERAS di awal.

FORMAT OUTPUT: Rapi dan mudah dibaca
[KATEGORI] | [TINGKAT KEPARAHAN]
Analisis Visual: [penjelasan singkat] \n
Analisis Keluhan: [penjelasan singkat] \n
Indikasi/Kemungkinan: [diagnosa indikatif, jika ada] \n
Rekomendasi: [departemen spesialis] \n
Tindakan: [saran segera] \n
"""

def triase_dengan_teks_saja():
    """Mode interaktif: pertanyaan teks saja"""
    print("\n" + "="*50)
    print("📝 MODE TRIASE TEXT (Ketik 'keluar' untuk berhenti)")
    print("="*50 + "\n")
    
    while True:
        pertanyaan = input("Pasien: ").strip()
        if pertanyaan.lower() == 'keluar':
            break
        
        if not pertanyaan:
            print("Masukkan pertanyaan terlebih dahulu!\n")
            continue
            
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=pertanyaan,
                config=types.GenerateContentConfig(
                    system_instruction=INSTRUKSI_MEDIS_UNIFIED,
                    temperature=0.3
                )
            )
            
            print(f"\n🏥 HASIL TRIASE:\n{response.text}\n")
            print("-" * 50 + "\n")
        except Exception as e:
            if "503" in str(e):
                print("Server sibuk. Mencoba lagi dalam 5 detik...")
                time.sleep(5)
            else:
                print(f"❌ Error: {e}\n")

def triase_dengan_gambar_dan_teks():
    """Mode: analisis gambar + teks"""
    print("\n" + "="*50)
    print("📸 MODE TRIASE VISUAL (Gambar + Teks)")
    print("="*50 + "\n")
    
    # Input path gambar
    path_gambar = input("Masukkan path/nama file gambar (contoh: gejala.jpg): ").strip()
    
    if not os.path.exists(path_gambar):
        print(f"❌ File '{path_gambar}' tidak ditemukan!")
        return
    
    # Input pertanyaan pasien
    pertanyaan = input("Deskripsi gejala/keluhan pasien: ").strip()
    
    if not pertanyaan:
        print("❌ Masukkan deskripsi gejala terlebih dahulu!")
        return
    
    try:
        # Buka gambar
        img = Image.open(path_gambar)
        print(f"\n✓ Gambar berhasil dibaca: {path_gambar}")
        print("🔄 Sedang menganalisis gambar dan teks...\n")
        
        # Analisis gambar + teks sekaligus
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[img, pertanyaan],  # Gabungkan gambar dan teks
            config=types.GenerateContentConfig(
                system_instruction=INSTRUKSI_MEDIS_UNIFIED,
                temperature=0.3
            )
        )
        
        print(f"🏥 HASIL TRIASE VISUAL:\n{response.text}\n")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ Error: {e}")

def menu_utama():
    """Menu interaktif untuk memilih mode"""
    while True:
        print("\n" + "="*50)
        print("🏥 ANTIGRAVITY HEALTH AGENT - TRIASE MEDIS")
        print("="*50)
        print("\nPilih mode:")
        print("1️⃣  - Triase Teks Saja (Pertanyaan gejala interaktif)")
        print("2️⃣  - Triase Visual (Analisis gambar + teks)")
        print("0️⃣  - Keluar")
        print("-"*50)
        
        pilihan = input("Pilihan Anda (0-2): ").strip()
        
        if pilihan == "1":
            triase_dengan_teks_saja()
        elif pilihan == "2":
            triase_dengan_gambar_dan_teks()
        elif pilihan == "0":
            print("\n✋ Terima kasih telah menggunakan Antigravity Health Agent!")
            break
        else:
            print("❌ Pilihan tidak valid! Silakan masukkan 0, 1, atau 2.")

if __name__ == "__main__":
    menu_utama()
