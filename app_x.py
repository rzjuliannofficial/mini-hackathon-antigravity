from google import genai
from google.genai import types
from PIL import Image
import os
from dotenv import load_dotenv
import time
import json
import math

# Load variabel dari file .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Pastikan API_KEY terbaca
if not API_KEY:
    print("Error: API Key tidak ditemukan di file .env!")
    exit()

client = genai.Client(api_key=API_KEY)

# --- KOORDINAT USER (POLINEMA MALANG) ---
LAT_USER = -7.9467136
LON_USER = 112.6156123

# --- LANGKAH 1: DEFINISI TOOLS ---

def hitung_jarak(lat1, lon1, lat2, lon2):
    """Menghitung jarak menggunakan Haversine Formula (dalam KM)"""
    R = 6371  # Radius bumi dalam KM
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def cari_puskesmas_terdekat(lokasi_user: str):
    """Mencari 5 rumah sakit/puskesmas terdekat berdasarkan koordinat Polinema Malang."""
    print(f"\n[LOG]: Agen memanggil fungsi pencarian lokasi untuk: {lokasi_user}")
    
    try:
        # Baca data dari database_5rs.json
        with open('database/database_5rs.json', 'r', encoding='utf-8') as f:
            data_rs = json.load(f)
        
        # Hitung jarak dari Polinema ke setiap RS
        for rs in data_rs:
            rs['jarak_km'] = hitung_jarak(LAT_USER, LON_USER, rs['lat'], rs['lon'])
            # Format jarak untuk tampilan
            if rs['jarak_km'] < 1:
                rs['jarak_display'] = f"{rs['jarak_km']*1000:.0f}m"
            else:
                rs['jarak_display'] = f"{rs['jarak_km']:.2f}km"
        
        # Urutkan berdasarkan jarak terkecil
        data_terurut = sorted(data_rs, key=lambda x: x['jarak_km'])
        
        # Ambil 5 teratas
        hasil_terdekat = data_terurut[:5]
        
        # Format hasil untuk respon
        formatted_data = []
        for idx, rs in enumerate(hasil_terdekat, 2):
            formatted_data.append({
                "nomor": idx,
                "nama": rs['nama_rs'],
                "tipe_kelas": rs['tipe_kelas'],
                "kota": rs['kota_kab'],
                "alamat": rs['alamat'],
                "telepon": rs['telepon'],
                "jarak": rs['jarak_display'],
                "jarak_km": rs['jarak_km']
            })
        
        return {
            "status": "success",
            "lokasi_user": f"Polinema Malang ({LAT_USER}, {LON_USER})",
            "data": formatted_data,
            "total_faskes": len(formatted_data)
        }
    
    except FileNotFoundError:
        print("[ERROR]: File database_5rs.json tidak ditemukan!")
        return {
            "status": "error",
            "pesan": "Database fasilitas kesehatan tidak ditemukan"
        }

def kirim_data_ke_faskes(nama_pasien: str, kategori: str, ringkasan_gejala: str, faskes_tujuan: str):
    """Mengintegrasikan data triase ke sistem JKN/Rumah Sakit untuk pendaftaran otomatis."""
    print(f"\n[INTEGRASI]: Menghubungkan ke API JKN Mobile...")
    print(f"[LOG]: Mengirim data pasien {nama_pasien} ke {faskes_tujuan}...")
    
    # Di sini nantinya kamu pakai library 'requests' untuk tembak API Laravel-mu
    # Simulasi sukses:
    import random
    nomor_antrean = f"A-{random.randint(100, 999)}"
    prioritas_text = "(PRIORITAS)" if kategori in ["MERAH", "KUNING"] else "(NORMAL)"
    
    return {
        "status": "Terintegrasi",
        "nomor_antrean": f"{nomor_antrean} {prioritas_text}",
        "pesan": f"Data triase {kategori} telah diterima {faskes_tujuan}. Dokter jaga telah dinotifikasi.",
        "waktu_pendaftaran": time.strftime("%Y-%m-%d %H:%M:%S")
    }

# --- LANGKAH 2: KONFIGURASI AGEN ---

INSTRUKSI_MEDIS_UNIFIED = """
Anda adalah 'Antigravity Health Agent' - Agen triase medis terpadu dengan integrasi lokasi dan pendaftaran otomatis.

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
7. Jika KUNING/MERAH:
   - WAJIB panggil 'cari_puskesmas_terdekat' dengan lokasi pasien.
   - SETELAH dapat lokasi, WAJIB panggil 'kirim_data_ke_faskes' untuk mendaftarkan pasien secara otomatis.
8. Berikan nomor antrean kepada pasien sebagai bukti pendaftaran JKN Mobile.

FORMAT OUTPUT: Rapi dan mudah dibaca
[KATEGORI] | [TINGKAT KEPARAHAN]
Analisis Visual: [penjelasan singkat] \n
Analisis Keluhan: [penjelasan singkat] \n
Indikasi/Kemungkinan: [diagnosa indikatif, jika ada] \n
Rekomendasi: [departemen spesialis] \n
Tindakan: [saran segera] \n
Lokasi Terdekat: [nama faskes + jarak] \n
"""

# Daftar tools yang tersedia
tools_kesehatan = [cari_puskesmas_terdekat, kirim_data_ke_faskes]

# --- LANGKAH 3: MODE-MODE TRIASE ---

def triase_dengan_teks_saja():
    """Mode interaktif: pertanyaan teks saja"""
    print("\n" + "="*60)
    print("📝 MODE TRIASE TEXT (Ketik 'keluar' untuk berhenti)")
    print("="*60 + "\n")
    
    while True:
        print("📋 Informasi yang dibutuhkan:")
        nama_pasien = input("Nama pasien: ").strip()
        if nama_pasien.lower() == 'keluar':
            break
        
        lokasi = input("Lokasi pasien (kota/area): ").strip()
        pertanyaan = input("Keluhan/gejala pasien: ").strip()
        
        if not nama_pasien or not lokasi or not pertanyaan:
            print("❌ Semua informasi harus diisi!\n")
            continue
            
        try:
            # Tambahkan informasi langsung ke prompt
            prompt_lengkap = f"""
INFORMASI PASIEN:
- Nama: {nama_pasien}
- Lokasi: {lokasi}
- Keluhan: {pertanyaan}

Lakukan triase berdasarkan informasi di atas.
"""
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt_lengkap,
                config=types.GenerateContentConfig(
                    system_instruction=INSTRUKSI_MEDIS_UNIFIED,
                    tools=tools_kesehatan,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False),
                    temperature=0.3
                )
            )
            
            print(f"\n🏥 HASIL TRIASE:\n{response.text}\n")
            print("-" * 60 + "\n")
        except Exception as e:
            if "503" in str(e):
                print("Server sibuk. Mencoba lagi dalam 5 detik...")
                time.sleep(5)
            else:
                print(f"❌ Error: {e}\n")

def triase_dengan_gambar_dan_teks():
    """Mode: analisis gambar + teks"""
    print("\n" + "="*60)
    print("📸 MODE TRIASE VISUAL (Gambar + Teks)")
    print("="*60 + "\n")
    
    # Input informasi pasien
    nama_pasien = input("Nama pasien: ").strip()
    lokasi = input("Lokasi pasien (kota/area): ").strip()
    
    # Input path gambar
    nama_file = input("Masukkan nama file gambar (contoh: gejala.jpg): ").strip()
    path_gambar = f"img/{nama_file}"
    
    if not os.path.exists(path_gambar):
        print(f"❌ File '{nama_file}' tidak ditemukan!")
        return
    
    # Input pertanyaan pasien
    pertanyaan = input("Deskripsi gejala/keluhan pasien: ").strip()
    
    if not nama_pasien or not lokasi or not pertanyaan:
        print("❌ Semua informasi harus diisi!")
        return
    
    try:
        # Buka gambar
        img = Image.open(path_gambar)
        print(f"\n✓ Gambar berhasil dibaca: {path_gambar}")
        print("🔄 Sedang menganalisis gambar dan teks...\n")
        
        # Buat prompt lengkap dengan info pasien
        prompt_lengkap = f"""
INFORMASI PASIEN:
- Nama: {nama_pasien}
- Lokasi: {lokasi}
- Keluhan: {pertanyaan}

Analisis gambar di atas beserta informasi pasien untuk melakukan triase.
"""
        
        # Analisis gambar + teks sekaligus dengan tools
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[img, prompt_lengkap],
            config=types.GenerateContentConfig(
                system_instruction=INSTRUKSI_MEDIS_UNIFIED,
                tools=tools_kesehatan,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False),
                temperature=0.3
            )
        )
        
        print(f"🏥 HASIL TRIASE VISUAL:\n{response.text}\n")
        print("-" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")

def triase_cepat_demo():
    """Mode demo: Simulasi triase cepat dengan kasus-kasus contoh"""
    print("\n" + "="*60)
    print("⚡ MODE DEMO TRIASE CEPAT (Kasus Preset)")
    print("="*60 + "\n")
    
    kasus_demo = {
        "1": {
            "nama": "Budi Santoso",
            "lokasi": "Lowokwaru, Malang",
            "gejala": "Saya kecelakaan motor, ada luka di tangan dan kepala berdarah hebat!"
        },
        "2": {
            "nama": "Siti Rahmawati",
            "lokasi": "Dinoyo, Malang",
            "gejala": "Demam tinggi 39°C, batuk berdahak hijau, sesak nafas sejak 2 hari"
        },
        "3": {
            "nama": "Ahmad Ridho",
            "lokasi": "Klojen, Malang",
            "gejala": "Sakit perut biasa saja, tidak ada demam. Sudah 2 hari begini"
        }
    }
    
    print("Pilih kasus demo:")
    for key, value in kasus_demo.items():
        print(f"{key}. {value['nama']} - {value['gejala'][:40]}...")
    print("0. Kembali ke menu utama")
    
    pilihan = input("\nPilihan Anda: ").strip()
    
    if pilihan not in kasus_demo:
        if pilihan != "0":
            print("❌ Pilihan tidak valid!")
        return
    
    kasus = kasus_demo[pilihan]
    
    try:
        prompt_lengkap = f"""
INFORMASI PASIEN:
- Nama: {kasus['nama']}
- Lokasi: {kasus['lokasi']}
- Keluhan: {kasus['gejala']}

Lakukan triase lengkap dengan pencarian lokasi fasilitas kesehatan terdekat.
"""
        
        print("\n🔄 Sedang melakukan triase...\n")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_lengkap,
            config=types.GenerateContentConfig(
                system_instruction=INSTRUKSI_MEDIS_UNIFIED,
                tools=tools_kesehatan,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False),
                temperature=0.3
            )
        )
        
        print(f"🏥 HASIL TRIASE:\n{response.text}\n")
        print("-" * 60)
        
    except Exception as e:
        if "503" in str(e):
            print("Server sibuk. Mencoba lagi dalam 5 detik...")
            time.sleep(5)
        else:
            print(f"❌ Error: {e}\n")

# --- LANGKAH 4: MENU UTAMA ---

def menu_utama():
    """Menu interaktif untuk memilih mode"""
    while True:
        print("\n" + "="*60)
        print("🏥 ANTIGRAVITY HEALTH AGENT - TRIASE MEDIS TERPADU")
        print("="*60)
        print("\n📋 Pilih mode layanan:")
        print("1️⃣  - Triase Teks (Pertanyaan gejala interaktif)")
        print("2️⃣  - Triase Visual (Analisis gambar + teks)")
        print("3️⃣  - Demo Triase Cepat (Kasus preset)")
        print("0️⃣  - Keluar")
        print("-"*60)
        
        pilihan = input("\n👉 Pilihan Anda (0-3): ").strip()
        
        if pilihan == "1":
            triase_dengan_teks_saja()
        elif pilihan == "2":
            triase_dengan_gambar_dan_teks()
        elif pilihan == "3":
            triase_cepat_demo()
        elif pilihan == "0":
            print("\n✋ Terima kasih telah menggunakan Antigravity Health Agent!")
            print("💙 Stay healthy!\n")
            break
        else:
            print("❌ Pilihan tidak valid! Silakan masukkan 0, 1, 2, atau 3.")

if __name__ == "__main__":
    menu_utama()
