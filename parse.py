from bs4 import BeautifulSoup
import json
import re

# Masukkan semua data HTML yang kamu copy ke dalam file 'data_mentah.html'
def html_to_json(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Kita tambahkan tag table agar soup bisa membaca dengan sempurna
    soup = BeautifulSoup(f"<table>{html_content}</table>", 'html.parser')
    rows = soup.find_all('tr')
    
    daftar_rs = []
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 7:
            # Ambil Kode RS dari link profil (angka di akhir URL)
            link_profile = cols[7].find('a')['href'] if cols[7].find('a') else ""
            kode_rs = link_profile.split('/')[-1] if link_profile else ""
            
            data = {
                "nama_rs": cols[0].get_text(strip=True),
                "provinsi": cols[1].get_text(strip=True),
                "kota_kab": cols[2].get_text(strip=True),
                "alamat": cols[3].get_text(strip=True),
                "telepon": cols[4].get_text(strip=True),
                "pemilik": cols[5].get_text(strip=True),
                "tipe_kelas": cols[6].get_text(strip=True),
                "kode_rs": kode_rs  # Ini KTP-nya rumah sakit untuk JKN!
            }
            daftar_rs.append(data)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(daftar_rs, f, indent=4)
    
    print(f"Selesai! {len(daftar_rs)} Rumah Sakit berhasil diringkas ke {output_file}")

if __name__ == "__main__":
    html_to_json('data_mentah.html', 'database_rs.json')