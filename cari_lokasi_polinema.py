import json
import math

# Koordinat Polinema Malang (User Location)
LAT_USER = -7.9467136
LON_USER = 112.6156123

def hitung_jarak(lat1, lon1, lat2, lon2):
    """Menghitung jarak menggunakan Haversine Formula (dalam KM)"""
    R = 6371  # Radius bumi dalam KM
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def cari_faskes_terdekat(lat_user, lon_user, jumlah=5):
    """
    Mencari fasilitas kesehatan terdekat dari lokasi user.
    Default menampilkan 5 terdekat.
    """
    # Database Faskes di Malang dengan koordinat
    data_faskes = [
        {
            "nama_rs": "RSUB Malang (Rumah Sakit Universitas Brawijaya)",
            "kota": "Malang",
            "alamat": "Jl. Soekarno Hatta No. 28",
            "telepon": "0341-679790",
            "tipe": "Rumah Sakit Umum",
            "lat": -7.9500,
            "lon": 112.6000
        },
        {
            "nama_rs": "Puskesmas Lowokwaru",
            "kota": "Malang",
            "alamat": "Jl. Tretes No. 10, Lowokwaru",
            "telepon": "0341-342891",
            "tipe": "Puskesmas",
            "lat": -7.9520,
            "lon": 112.6250
        },
        {
            "nama_rs": "RS Saiful Anwar Malang",
            "kota": "Malang",
            "alamat": "Jl. Jaksa Agung Suprapto No. 10",
            "telepon": "0341-363333",
            "tipe": "Rumah Sakit Umum",
            "lat": -7.9750,
            "lon": 112.6350
        },
        {
            "nama_rs": "Klinik Kesehatan Citra Medika",
            "kota": "Malang",
            "alamat": "Jl. Puncak No. 5, Klojen",
            "telepon": "0341-881888",
            "tipe": "Klinik Kesehatan",
            "lat": -7.9650,
            "lon": 112.6100
        },
        {
            "nama_rs": "RS Panti Waluya Malang",
            "kota": "Malang",
            "alamat": "Jl. Mayjen Panjaitan No. 139",
            "telepon": "0341-362881",
            "tipe": "Rumah Sakit Umum",
            "lat": -7.9400,
            "lon": 112.5950
        },
        {
            "nama_rs": "Puskesmas Klojen",
            "kota": "Malang",
            "alamat": "Jl. Flamboyan Raya, Klojen",
            "telepon": "0341-356789",
            "tipe": "Puskesmas",
            "lat": -7.9680,
            "lon": 112.6150
        },
        {
            "nama_rs": "RS Bhakti Yasa Malang",
            "kota": "Malang",
            "alamat": "Jl. Joyo Raharjo No. 56",
            "telepon": "0341-484848",
            "tipe": "Rumah Sakit Umum",
            "lat": -7.9300,
            "lon": 112.6200
        },
        {
            "nama_rs": "Klinik Kesehatan Dinoyo",
            "kota": "Malang",
            "alamat": "Jl. Raya Dinoyo No. 123",
            "telepon": "0341-451234",
            "tipe": "Klinik Kesehatan",
            "lat": -7.9450,
            "lon": 112.5850
        }
    ]
    
    # Hitung jarak untuk setiap faskes
    for faskes in data_faskes:
        faskes['jarak'] = hitung_jarak(lat_user, lon_user, faskes['lat'], faskes['lon'])
    
    # Urutkan berdasarkan jarak terkecil
    data_terurut = sorted(data_faskes, key=lambda x: x['jarak'])
    
    # Ambil sejumlah teratas
    return data_terurut[:jumlah]

def tampilkan_hasil(hasil, lokasi_asli="Polinema Malang"):
    """Menampilkan hasil pencarian dengan format yang rapi"""
    print("\n" + "="*80)
    print(f"📍 FASILITAS KESEHATAN TERDEKAT DARI {lokasi_asli.upper()}")
    print(f"   Koordinat: ({LAT_USER}, {LON_USER})")
    print("="*80 + "\n")
    
    for idx, faskes in enumerate(hasil, 1):
        print(f"{idx}. {faskes['nama_rs']}")
        print(f"   📍 Tipe: {faskes['tipe']}")
        print(f"   📮 Alamat: {faskes['alamat']}")
        print(f"   📞 Telepon: {faskes['telepon']}")
        print(f"   📏 Jarak: {faskes['jarak']:.2f} KM")
        print(f"   🗺️  Koordinat: ({faskes['lat']}, {faskes['lon']})")
        print()

def export_ke_json(hasil, nama_file="faskes_terdekat.json"):
    """Export hasil pencarian ke file JSON"""
    with open(nama_file, 'w', encoding='utf-8') as f:
        json.dump(hasil, f, indent=2, ensure_ascii=False)
    print(f"✅ Hasil telah disimpan ke {nama_file}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("🔍 Memulai pencarian fasilitas kesehatan terdekat dari Polinema Malang...\n")
    
    # Cari 5 faskes terdekat
    hasil = cari_faskes_terdekat(LAT_USER, LON_USER, jumlah=5)
    
    # Tampilkan hasil
    tampilkan_hasil(hasil)
    
    # Optional: Export ke JSON
    print("-"*80)
    simpan = input("\n💾 Simpan hasil ke JSON? (y/n): ").strip().lower()
    if simpan == 'y':
        export_ke_json(hasil, "faskes_terdekat_polinema.json")
        print("✅ Siap digunakan untuk integrasi dengan app_x.py")
