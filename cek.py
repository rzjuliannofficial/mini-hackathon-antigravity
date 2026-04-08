from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Mencoba menarik data model...")
try:
    # Kita ambil 10 model pertama secara paksa
    response = client.models.list(config={'page_size': 10})
    
    models = list(response) # Paksa ubah ke list
    if not models:
        print("Sistem mengembalikan hasil kosong. Cek API Key/Project Anda!")
    else:
        for m in models:
            print(f"- {m.name} (Actions: {m.supported_actions})")
except Exception as e:
    print(f"Error fatal: {e}")