from machine import I2C, Pin
import time
i2c = I2C (0, scl=Pin(22), sda=Pin(21), freq=100_000)
DHT12_ADDR = 0x5c
# --- Lecture du DHT12 ---
def read_dht12():
    try:
        # On écrit 0x00 pour pointer sur le registre de données
        i2c.writeto(DHT12_ADDR, b'\x00')
        data = i2c.readfrom(DHT12_ADDR, 5)
        hum = data[0] + data[1] / 10
        temp = data[2] + (data[3] & 0x7F) / 10
        if data[3] & 0x80:  # bit signe température
            temp = -temp
        # Vérif checksum (facultative)
        chk = (data[0] + data[1] + data[2] + data[3]) & 0xFF
        if chk != data[4]:
            raise ValueError("Checksum invalid")
        return temp, hum
    except Exception as e:
        print("Error DHT12:", e)
        return None, None

# --- Main ---
try:
    while True:
        temp, hum = read_dht12()
        if temp is not None:
            print(f"{temp:.1f}°C | {hum:.1f}%")
        time.sleep(2)
except KeyboardInterrupt:
    print("Program has stopped.")
