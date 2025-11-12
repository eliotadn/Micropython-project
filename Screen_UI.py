from machine import Pin, I2C
from rotary_irq import RotaryIRQ
from sh1106 import SH1106_I2C
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = SH1106_I2C(i2c)
oled.fill(0)
oled.show()

r = RotaryIRQ(pin_num_clk=18, pin_num_dt=19, min_val=0, max_val=999,
              reverse=False, range_mode=RotaryIRQ.RANGE_WRAP)

val_prec = r.value()

while True:
    val = r.value()
    if val != val_prec:
        val_prec = val
        oled.fill(0)
        oled.text(str(val), 50, 30)
        oled.show()
    time.sleep_ms(50)
