# 🚀 Setup Antigravity Health System (Laravel + Python API)

## 📋 Struktur Project

```
mini-hackathon-antigravity/
├── python-app/                    ← Python API dengan AI (Gemini)
│   ├── venv/
│   ├── app_x.py                   ← Main app dengan integrasi HTTP ke Laravel
│   ├── database/
│   └── .env
│
└── mini-hackathon/                ← Laravel Backend
    ├── app/
    ├── routes/api.php             ← API Endpoint untuk Python
    ├── routes/web.php             ← Dashboard Web
    ├── database/migrations/        ← Tabel triage_registrations
    ├── resources/views/
    │   ├── dashboard-triage.blade.php    ← Dashboard real-time
    │   └── layouts/app.blade.php
    └── .env
```

---

## 🔧 SETUP LANGKAH DEMI LANGKAH

### **1. Setup Laravel**

```bash
cd mini-hackathon-antigravity/mini-hackathon

# Copy .env
cp .env.example .env

# Generate application key
php artisan key:generate

# Jalankan migration (buat tabel triage_registrations)
php artisan migrate
```

**Konfigurasi di `.env` (sesuaikan dengan database Anda):**
```
DB_CONNECTION=pgsql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=mini_hackathon
DB_USERNAME=postgress
DB_PASSWORD= # Sesuaikan dengan password PostgreSQL Anda
```

### **2. Setup Python (requests library)**

```bash
cd /python-app

# Pastikan venv sudah aktif
.\venv\Scripts\Activate.ps1

# Install requests jika belum ada
pip install requests

# Update .env dengan GEMINI_API_KEY jika belum ada
```

---

## ▶️ MENJALANKAN SISTEM

### **Terminal 1: Jalankan Laravel**

```bash
cd mini-hackathon-antigravity/mini-hackathon
php artisan serve
```

**Output:**
```
Laravel development server started on http://127.0.0.1:8000
```

### **Terminal 2: Jalankan Python AI**

```bash
cd mini-hackathon-antigravity/python-app
.\venv\Scripts\Activate.ps1
python app_x.py
```

---

## 🌐 AKSES APLIKASI

### **Dashboard Web (Monitoring Real-time)**
- **URL:** http://127.0.0.1:8000
- **Fitur:** Lihat tabel triase, statistik kategori, nomor antrean

### **API Endpoints** (untuk Python)
- **POST /api/triage-registration** ← Python kirim data ke sini
- **GET /api/triage/registrations** ← Dashboard ambil data dari sini
- **GET /api/triage/registrations/{id}** ← Detail satu triase

---

## 🔄 ALUR KERJA INTEGRASI

### **1. User Input di Python**
```
User: "Perut saya sakit"
     ↓
[Gemini AI melakukan triase & kategorisasi]
     ↓
Kategori: KUNING
RS Tujuan: RSUD Kota Malang
```

### **2. Python POST ke Laravel**
```python
POST http://127.0.0.1:8000/api/triage-registration

{
    "nama": "Budi",
    "kategori": "KUNING",
    "gejala": "Nyeri perut akut bagian bawah",
    "rs_tujuan": "RSUD Kota Malang"
}
```

### **3. Laravel Generate Nomor Antrean & Simpan DB**
```json
{
    "status": "success",
    "nomor_antrean": "TRIAGE-20250411125645-123",
    "prioritas": "PRIORITAS",
    "kategori": "KUNING"
}
```

### **4. Dashboard Auto-Update (Polling setiap 3 detik)**
```
✅ Baris baru muncul di tabel
✅ Statistik kategori terupdate
✅ Perawat langsung lihat pasien baru
```

---

## 🔍 TESTING

### **Test 1: Cek API Laravel**
```bash
# Di PowerShell/CMD
curl -X GET http://127.0.0.1:8000/api/triage/registrations
```

**Expected Output:**
```json
{
    "status": "success",
    "data": {
        "data": [],
        "links": {...}
    }
}
```

### **Test 2: POST Data dari Python (Manual)**
```python
import requests

url = "http://127.0.0.1:8000/api/triage-registration"
data = {
    "nama": "Test User",
    "kategori": "MERAH",
    "gejala": "Kesulitan bernapas",
    "rs_tujuan": "RSUD Kota Malang"
}

response = requests.post(url, json=data)
print(response.json())
```

### **Test 3: Refresh Dashboard**
- Buka http://127.0.0.1:8000 di browser
- Data yang dikirim dari Python sudah tampil di tabel ✅

---

## 📊 STRUKTUR DATABASE (triage_registrations)

| Column | Type | Keterangan |
|--------|------|-----------|
| id | INT | Primary Key |
| nama_pasien | VARCHAR | Nama pasien |
| kategori | ENUM | MERAH/KUNING/HIJAU/BIRU |
| gejala | TEXT | Ringkasan gejala |
| rs_tujuan | VARCHAR | Rumah sakit tujuan |
| nomor_antrean | VARCHAR | Nomor antrean unik (generated) |
| lokasi_user | VARCHAR | Koordinat lokasi user (optional) |
| jarak_km | INT | Jarak ke RS (optional) |
| status | ENUM | pending/confirmed/processed |
| created_at | TIMESTAMP | Waktu registrasi |
| updated_at | TIMESTAMP | Waktu update |

---

## ⚠️ TROUBLESHOOTING

### **Error: "Koneksi ke Laravel gagal"**
**Solusi:**
1. Pastikan Laravel sudah `php artisan serve` dan running di http://127.0.0.1:8000
2. Cek port 8000 tidak digunakan: `netstat -ano | findstr :8000`
3. Jika port 8000 busy, gunakan: `php artisan serve --port=8001` dan update URL di `app_x.py`

### **Error: "Database table not found"**
**Solusi:**
```bash
cd mini-hackathon/
php artisan migrate --fresh  # Recreate all tables
```

### **Dashboard tidak auto-update**
**Solusi:**
1. Cek browser console (F12) untuk error
2. Pastikan API endpoint `/api/triage/registrations` aktif
3. Refresh halaman (Ctrl+F5)

### **Python app tidak bisa import requests**
**Solusi:**
```bash
.\venv\Scripts\Activate.ps1
pip install requests
```

---

## 🚀 NEXT STEPS (Advanced)

1. **Livewire untuk Real-time Update** (built-in)
   - Update `resources/views/dashboard-triage.blade.php` pakai Livewire polling
   
2. **WebSocket untuk Live Streaming** 
   - Setup Laravel Echo + Pusher untuk update tanpa polling
   
3. **Notification System**
   - Alert perawat ketika ada pasien MERAH masuk
   
4. **Mobile App**
   - Flutter/React Native untuk registrasi pasien
   
5. **Analytics Dashboard**
   - Grafik distribusi kategori, waktu rata-rata tunggu, dll

---

**Selamat! Sistem Antigravity Health sudah siap digunakan! 🎉**
