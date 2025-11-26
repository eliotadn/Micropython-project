import time

DHT12_ADDR = 0x5c

def read_dht12(i2c):
    """Reads temperature and humidity via the provided I2C object"""
    try:
        i2c.writeto(DHT12_ADDR, b'\x00')
        data = i2c.readfrom(DHT12_ADDR, 5)
        
        hum = data[0] + data[1] / 10
        temp = data[2] + (data[3] & 0x7F) / 10
        
        if data[3] & 0x80:
            temp = -temp
            
        chk = (data[0] + data[1] + data[2] + data[3]) & 0xFF
        if chk != data[4]:
            return None, None
            
        return temp, hum
    except Exception as e:

        return None, None
