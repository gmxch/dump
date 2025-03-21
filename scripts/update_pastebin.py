import requests
import os
import hashlib
from datetime import datetime

# Ambil API Key & User Key dari GitHub Secrets
API_KEY = os.getenv("PASTEBIN_API_KEY")
USER_KEY = os.getenv("PASTEBIN_USER_KEY")
PASTE_ID = os.getenv("PASTE_ID")

# Cek apakah variabel lingkungan tersedia
if not API_KEY or not USER_KEY or not PASTE_ID:
    print("❌ Error: Pastikan API Key, User Key, dan Paste ID tersedia!")
    exit(1)

# Generate password berdasarkan format MMDDHH (Bulan, Tanggal, Jam UTC)
today_date = datetime.utcnow().strftime("%m%d%H")  
today_password = hashlib.sha256(today_date.encode()).hexdigest()[:8]  # Ambil 8 karakter pertama dari hash

# Format isi Pastebin (dengan "PASSWORD=")
paste_content = f"PASSWORD={today_password}"

# Update Pastebin dengan password baru
data = {
    "api_dev_key": API_KEY,
    "api_user_key": USER_KEY,
    "api_paste_key": PASTE_ID,
    "api_option": "edit",
    "api_paste_code": paste_content  # Simpan dalam format "PASSWORD=..."
}

# Kirim request ke Pastebin
response = requests.post("https://pastebin.com/api/api_post.php", data=data)

if response.status_code == 200 and "Bad API request" not in response.text:
    print("✅ Pastebin updated successfully!")
else:
    print("❌ Failed to update:", response.text)
