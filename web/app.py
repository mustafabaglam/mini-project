import json
import os
import sys
import threading
import logging
from flask import Flask
from flask_socketio import SocketIO
import serial

PORT = int(os.environ.get('PORT', 3000))

if sys.platform.startswith('win'):
    SERIAL_PATH = 'COM3'
elif sys.platform.startswith('darwin'):
    SERIAL_PATH = '/dev/tty.usbmodem14101'
else:
    SERIAL_PATH = '/dev/ttyACM0'


def find_free_port(start_port):
    import socket
    port = start_port
    while port < 65535:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(('0.0.0.0', port))
                return port
            except OSError:
                port += 1
    raise OSError('No available port found starting from %s' % start_port)

BAUD_RATE = 9600

app = Flask(__name__, static_folder='public', static_url_path='')
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

@app.route('/')
def index():
    return app.send_static_file('index.html')


def serial_reader():
    try:
        with serial.Serial(SERIAL_PATH, BAUD_RATE, timeout=1) as ser:
            logging.info('Arduino bağlı: %s', SERIAL_PATH)
            buffer = ''
            while True:
                raw = ser.read(ser.in_waiting or 1)
                if not raw:
                    continue
                try:
                    buffer += raw.decode('utf-8', errors='ignore')
                except Exception:
                    continue
                lines = buffer.split('\n')
                buffer = lines.pop()
                for line in lines:
                    trimmed = line.strip()
                    if not trimmed:
                        continue
                    try:
                        payload = json.loads(trimmed)
                        logging.info('gönderiliyor: %s', trimmed)
                        socketio.emit('message', json.dumps(payload))
                    except json.JSONDecodeError:
                        logging.warning('geçersiz veri: %s', trimmed)
    except serial.SerialException as exc:
        logging.error('Seri port hatası: %s', exc)
    except Exception as exc:
        logging.error('Seri port okuyucusunda hata: %s', exc)


if __name__ == '__main__':
    thread = threading.Thread(target=serial_reader, daemon=True)
    thread.start()
    PORT = find_free_port(PORT)
    logging.info('Sunucu çalışıyor: http://localhost:%s', PORT)
    socketio.run(app, host='0.0.0.0', port=PORT)
