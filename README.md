# Arduino Radar

Arduino + HC-SR04 ultrasonik sensör + servo motor kullanarak gerçek zamanlı radar görselleştirmesi yapan bir proje. Sensör verileri USB seri port üzerinden Node.js'e aktarılır, Socket.IO ile tarayıcıya iletilir ve Raphael SVG kütüphanesiyle görsel olarak çizilir.

Orijinal proje: [indiejoseph/Radar](https://github.com/indiejoseph/Radar)

---

## Gereksinimler

### Donanım
- Arduino (Uno veya benzeri)
- HC-SR04 ultrasonik mesafe sensörü
- Servo motor
- Bağlantı kabloları

### Devre Bağlantıları

| Bileşen | Arduino Pin |
|---|---|
| Servo sinyal | Pin 9 |
| HC-SR04 TRIG | Pin 12 |
| HC-SR04 ECHO | Pin 13 |

### Yazılım
- [Arduino IDE](https://www.arduino.cc/en/software)
- [Node.js](https://nodejs.org/) v18+
- Arduino kütüphanesi: **Ultrasonic** (Arduino IDE > Library Manager)

---

## Kurulum

### 1. Arduino Kütüphanesini Yükle

Arduino IDE'de: **Sketch > Include Library > Manage Libraries** → `Ultrasonic` ara ve yükle.

### 2. Arduino Sketch'i Yükle

`radar_ino/radar_ino.ino` dosyasını Arduino IDE ile açın ve kartınıza yükleyin.

### 3. Seri Port Adresini Ayarla

`web/app.js` dosyasındaki `SERIAL_PATH` değişkenini Arduino'nun bağlı olduğu porta göre düzenleyin:

```js
// Linux:
const SERIAL_PATH = '/dev/ttyUSB0'   // veya /dev/ttyACM0

// macOS:
const SERIAL_PATH = '/dev/tty.usbmodem...'

// Windows:
const SERIAL_PATH = 'COM3'
```

Seri port adresini bulmak için:
- **Linux/macOS:** `ls /dev/tty*` (Arduino bağlıyken ve bağlı değilken çalıştırıp farka bakın)
- **Windows:** Aygıt Yöneticisi > Bağlantı Noktaları

### 4. Bağımlılıkları Kur

```bash
cd web
npm install
```

---

## Çalıştırma

Arduino'yu bilgisayara bağladıktan sonra:

```bash
cd web
npm start
```

Tarayıcıda açın:

```
http://localhost:3000
```

Radar taraması gerçek zamanlı olarak ekranda görünmeye başlar.

---

## Proje Yapısı

```
├── radar_ino/
│   └── radar_ino.ino        # Arduino sketch (servo + ultrasonik sensör)
└── web/
    ├── app.js               # Node.js sunucusu (HTTP + Socket.IO + SerialPort)
    ├── package.json
    └── public/
        ├── index.html       # Tarayıcı arayüzü (CDN üzerinden kütüphane yükler)
        ├── css/
        │   └── style.css
        └── js/
            └── math.js      # Yardımcı matematik fonksiyonları
```

---

## Nasıl Çalışır

1. Arduino, servo motoru 0°–180° arasında 15°'lik adımlarla döndürür.
2. Her açıda HC-SR04 sensörü mesafeyi ölçer ve `{d:XX,r:YYY}` formatında seri porta yazar.
3. Node.js sunucusu seri portu dinler ve gelen veriyi Socket.IO üzerinden bağlı tarayıcılara iletir.
4. Tarayıcıdaki JavaScript, veriyi alarak Raphael SVG kütüphanesiyle radar ekranı üzerinde çizer.
