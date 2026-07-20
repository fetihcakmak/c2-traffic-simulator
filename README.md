<div align="center">
<pre>
   ___ ___     ___ _                 _      _           
  / __|_  )   / __(_)_ __ _  _ _ __ | |__ _| |_ ___ _ _ 
 | (__ / /   \__ \ | '  \ || | '  \| / _` |  _/ _ \ '_|
  \___/___|  |___/_|_|_|_\_,_|_|_|_|_\__,_|\__\___/_|  
</pre>
</div>

# 🚦 C2 Traffic Simulator

> Mavi takım (Blue Team) araçlarını ve IDS/IPS sistemlerini test etmek için sentetik Command & Control (C2) beacon trafiği üreten simülatör.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![Stdlib](https://img.shields.io/badge/Dep-Stdlib_Only-success)](./)
[![Status](https://img.shields.io/badge/Status-Active-success)](./)
[![Purpose](https://img.shields.io/badge/Purpose-Blue_Team_Testing-orange)](./)

---

## ⚠️ Yalnızca Yetkilendirilmiş Kullanım İçin

Bu araç, hedef adrese **gerçek HTTP/DNS istekleri gönderir** (yalnızca yerel/simüle bir çıktı üretmez). Cobalt Strike benzeri bir HTTP beacon profiliyle (User-Agent, URI desenleri, jitter'lı bekleme süreleri) trafik üretir; bu da onu IDS/IPS/EDR tespit kurallarını test etmek için gerçekçi kılar, ama aynı zamanda **yalnızca kendi sahip olduğunuz veya yazılı izniniz olan lab/test ortamlarına karşı** çalıştırılmalıdır. Üçüncü taraf sistemlere karşı kullanmak yasa dışıdır ve bu proje bunun için tasarlanmamıştır.

## 📈 Proje Hakkında

Mavi takımların IDS/IPS/EDR ürünlerini gerçek bir C2 kanalı kurmadan, sadece o kanala benzeyen trafik üreterek test etmesini sağlar. İki mod destekler:

- **HTTP Beacon** — Cobalt Strike varsayılan profiline benzer User-Agent, URI (`/api/v1/update`, `/submit.php`, `/jquery-3.3.1.min.js`) ve jitter'lı bekleme aralıklarıyla POST istekleri gönderir.
- **DNS Beacon** — Sorgu tabanlı (DNS tünelleme benzeri) beacon deseni üretir.

## 🧠 Nasıl Çalışır

```
main.py
  └── simulator/
        ├── http_beacon.py  ← Cobalt Strike profiliyle HTTP POST beacon üretici
        └── dns_beacon.py   ← DNS sorgu tabanlı beacon üretici
```

## ⚡ Kurulum

```bash
git clone https://github.com/fetihcakmak/c2-traffic-simulator.git
cd c2-traffic-simulator
python main.py --mode http --target http://127.0.0.1:8080 --count 3   # kendi lab ortamınıza karşı
```

## 🚀 Kullanım

```bash
# HTTP beacon (kendi test sunucunuza karşı)
python main.py --mode http --target http://192.168.1.5 --count 10

# DNS beacon (kendi test alan adınıza karşı)
python main.py --mode dns --target evil-lab.internal --count 5
```

## 🖥️ Örnek Çıktı

```
[HTTP] POST http://192.168.1.5/submit.php?id=4452 -> 403 (Sleep: 10.8s)
[HTTP] POST http://192.168.1.5/api/v1/update?id=4452 -> 403 (Sleep: 10.4s)
```

Hedef adres erişilemezse (bağlantı reddedilir/timeout) istek yine de denenir ve sonuç (`Connection Failed` veya HTTP durum kodu) loglanır — bu, IDS/IPS kurallarının paket seviyesinde tetiklenip tetiklenmediğini test etmek için yeterlidir.

## 📄 Lisans

Bu depo şu an bir lisans dosyası içermiyor. Kullanım koşulları için proje sahibiyle iletişime geçin.

---

*Fetih Çakmak — Cybersecurity Portfolio*
