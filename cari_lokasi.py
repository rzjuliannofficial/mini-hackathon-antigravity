from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- LANGKAH 1: DEFINISI TOOLS ---
def cari_puskesmas_terdekat(lokasi_user: str):
    """Mencari daftar puskesmas terdekat berdasarkan input lokasi."""
    print(f"\n[LOG]: Agen memanggil fungsi pencarian lokasi untuk: {lokasi_user}")
    # Simulasi data dari Database/Maps API
    return {
        "status": "success",
        "data": [
            {"nama": "Puskesmas Lowokwaru", "alamat": "Jl. Tretes No. 10", "jarak": "500m"},
            {"nama": "RSUB Malang", "alamat": "Jl. Soekarno Hatta", "jarak": "1.2km"}
        ]
    }

# --- LANGKAH 2: KONFIGURASI AGEN ---
INTRUKSI_SISTEM = """
Anda adalah Agen Triase Antigravity.
Protokol:
1. Analisis gejala pasien.
2. JIKA pasien berada dalam kategori KUNING atau MERAH, gunakan tool 'cari_puskesmas_terdekat'.
3. Berikan jawaban akhir yang menenangkan dan instruksi arah ke lokasi tersebut.
"""

def main():
    print("--- MULAI PERCAKAPAN AGEN ---")
    user_msg = "Tolong! Saya di daerah Lowokwaru, teman saya pingsan dan kepalanya berdarah!"

    # Memanggil model dengan Tools
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=user_msg,
        config=types.GenerateContentConfig(
            system_instruction=INTRUKSI_SISTEM,
            tools=[cari_puskesmas_terdekat],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
        )
    )

    print("\nRespon Akhir Agen:\n", response.text)

if __name__ == "__main__":
    main()