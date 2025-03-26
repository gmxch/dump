import requests
import os
import hashlib
from datetime import datetime

# Ambil API Key & User Key dari GitHub Secrets
API_KEY = os.getenv("PASTEBIN_API_KEY")
USER_KEY = os.getenv("PASTEBIN_USER_KEY")
PASTE_ID_LINKPASSWORD = os.getenv("PASTE_ID_LINKPASSWORD")
PASTE_ID_LINKKONTEN = os.getenv("PASTE_ID_LINKKONTEN")

# Cek apakah semua variabel tersedia
if not API_KEY or not USER_KEY or not PASTE_ID_LINKPASSWORD or not PASTE_ID_LINKKONTEN:
    print("❌ Error: Pastikan semua Secrets tersedia!")
    exit(1)

# Generate password berdasarkan format MMDDHH (Bulan, Tanggal, Jam UTC)
today_date = datetime.utcnow().strftime("%m%d%H")  
today_password = hashlib.sha256(today_date.encode()).hexdigest()[:8]  # Ambil 8 karakter pertama dari hash

# Update LinkPassword
data_password = {
    "api_dev_key": API_KEY,
    "api_user_key": USER_KEY,
    "api_paste_key": PASTE_ID_LINKPASSWORD,
    "api_option": "edit",
    "api_paste_code": f"PASSWORD={today_password}"
}
response_password = requests.post("https://pastebin.com/api/api_post.php", data=data_password)

# Update LinkKonten (mengganti password aksesnya)
data_konten = {
    "api_dev_key": API_KEY,
    "api_user_key": USER_KEY,
    "api_paste_key": PASTE_ID_LINKKONTEN,
    "api_option": "edit",
    "api_paste_private": "2",  # 2 = Private (hanya bisa diakses dengan password)
    "api_paste_password": today_password  # Password yang baru di-generate
}
response_konten = requests.post("https://pastebin.com/api/api_post.php", data=data_konten)

# Cek apakah berhasil diperbarui
if response_password.status_code == 200 and "Bad API request" not in response_password.text:
    print("✅ LinkPassword updated successfully!")
else:
    print("❌ Failed to update LinkPassword:", response_password.text)

if response_konten.status_code == 200 and "Bad API request" not in response_konten.text:
    print("✅ LinkKonten password updated successfully!")
else:
    print("❌ Failed to update LinkKonten:", response_konten.text)
