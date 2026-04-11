from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import json
import math

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
        # Baca data dari 5rs.json
        with open('5rs.json', 'r', encoding='utf-8') as f:
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
        for idx, rs in enumerate(hasil_terdekat, 3):
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
        print("[ERROR]: File 5rs.json tidak ditemukan!")
        return {
            "status": "error",
            "pesan": "Database fasilitas kesehatan tidak ditemukan"
        }

# --- LANGKAH 2: KONFIGURASI AGEN ---
INTRUKSI_SISTEM = """
Anda adalah Agen Triase Antigravity.
Protokol:
1. Analisis gejala pasien.
2. Tentukan kategori prioritas: MERAH (darurat), KUNING (segera), atau HIJAU (ringan).
3. JIKA pasien berada dalam kategori KUNING atau MERAH, WAJIB gunakan tool 'cari_puskesmas_terdekat'.
4. Fungsi ini akan mencari 5 fasilitas kesehatan terdekat dari Polinema Malang menggunakan koordinat real dan perhitungan Haversine.
5. Berikan jawaban akhir yang menenangkan, rekomendasi fasilitas terdekat, dan instruksi arah.
"""

def main():
    print("--- MULAI PERCAKAPAN AGEN ---")
    print(f"📍 User Location: Polinema Malang ({LAT_USER}, {LON_USER})")
    print()
    user_msg = "Tolong! Saya di Polinema, teman saya pingsan dan kepalanya berdarah!"

    # Memanggil model dengan Tools
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_msg,
        config=types.GenerateContentConfig(
            system_instruction=INTRUKSI_SISTEM,
            tools=[cari_puskesmas_terdekat],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
        )
    )

    print("\n🏥 Respon Akhir Agen:\n", response.text)
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
    
