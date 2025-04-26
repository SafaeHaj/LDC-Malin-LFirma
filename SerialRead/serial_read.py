import threading
import serial
import time
import json
from ..Backend.db.data_writer import write_all

_latest = None
_lock = threading.Lock()

def get_latest():
    with _lock:
        return _latest

def _read_loop(port='/dev/ttyACM0', baud=9600):
    global _latest
    ser = serial.Serial(port, baud, timeout=1)
    try:
        while True:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8').strip()
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                with _lock:
                    _latest = data
                write_all(data)
            time.sleep(0.01)
    finally:
        ser.close()

threading.Thread(target=_read_loop, daemon=True).start()
