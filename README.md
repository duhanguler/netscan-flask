# 🔍 NetScan Dashboard

![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-orange.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

NetScan Dashboard, yerel ağınızı tarayarak cihazları, açık portları ve servis bilgilerini listeleyen, modern görselleştirmelerle desteklenen bir **Flask** uygulamasıdır. 👨‍💻  
Kullanımı kolay arayüzü ile teknik ve teknik olmayan kullanıcılar için idealdir.

---

## 🚀 Özellikler

- 🔎 IP ve port aralığına göre ağ taraması
- 🖥️ Cihaz hostname/IP bilgisi ve açık portlar listesi
- 📊 Plotly ile port sayısı grafiği
- 📄 Sonuçları CSV olarak indirme
- 💡 Bootstrap 4 ile şık ve duyarlı arayüz

---

## ⚙️ Kurulum

### Gereksinimler

- Python 3.7+
- Nmap (sistemde kurulu ve PATH’e ekli olmalı)

### Adımlar

```bash
# 1. Repo'yu klonla
git clone https://github.com/kullanici_adiniz/netscan-flask-bootstrap.git
cd netscan-flask-bootstrap

# 2. Gerekli paketleri kur
pip install -r requirements.txt

# 3. Flask uygulamasını başlat
python app.py
