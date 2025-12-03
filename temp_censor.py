# Assuming DHT12 I2C sensor at address 0x5C
import time

def read_dht12(i2c):
    try:
        # 1. Request sensor data
        i2c.writeto(0x5C, b'\x00')
        time.sleep_ms(100) # Wait for conversion
        data = i2c.readfrom(0x5C, 5)
        
        # 2. Checksum validation
        if (data[0] + data[1] + data[2] + data[3]) & 0xFF == data[4]:
            # Data processing
            hum = data[0] + data[1] * 0.1
            temp = data[2] + (data[3] & 0x7F) * 0.1
            if data[3] & 0x80: # Handle negative temperatures
                temp = -temp
            return temp, hum
    except:
        pass
    return None, None
