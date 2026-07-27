import urllib.request
import json
import time
import random

# url = "https://m70204.belajarhub.id/django/api/sensor/"
url = "http://127.0.0.1:8000/api/sensor/"
api_key = "abc123"
device_id = "device01"

print("=== Pengiriman Data Sensor Django Otomatis Dimulai ===")

for i in range(1, 11):
    # Data suhu dan kelembapan realistis
    temp = round(random.uniform(25.0, 31.5), 1)
    hum = round(random.uniform(55.0, 72.0), 1)
    
    payload = {
        "apikey": api_key,
        "device_id": device_id,
        "temperature": temp,
        "humidity": hum
    }
    
    # Encode ke format JSON
    json_data = json.dumps(payload).encode('utf-8')
    
    # Request POST
    req = urllib.request.Request(url, data=json_data, method='POST')
    req.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req) as response:
            res_text = response.read().decode('utf-8')
            print(f"[{i}/10] Terkirim -> Suhu: {temp}°C, Kelembapan: {hum}%. Respon: {res_text}")
    except Exception as e:
        print(f"[{i}/10] Gagal mengirim data: {e}")
        
    time.sleep(1)

print("\n=== Pengiriman Data Selesai! ===")
print("Silakan cek halaman web Django Anda di:")
print("-> https://m70204.belajarhub.id/django/device/device01/")
print("-> https://m70204.belajarhub.id/django/device/device01/gauge/")
