# Assuming DHT12 I2C sensor at address 0x5C
import time

def read_dht12(i2c):
    try:
        i2c.writeto(0x5C, b'\x00')
        data = i2c.readfrom(0x5C, 5)
        
        # Checksum
        if (data[0] + data[1] + data[2] + data[3]) & 0xFF == data[4]:
            hum = data[0] + data[1] * 0.1
            temp = data[2] + (data[3] & 0x7F) * 0.1
            if data[3] & 0x80:
                temp = -temp
            return temp, hum
    except:
        pass
    return None, None
