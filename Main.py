from machine import Pin, I2C
from rotary_irq import RotaryIRQ
import time

# Custom Modules
import temp_censor
import Clock
import Screen_UI
import air_sensor

# --- CONFIGURATION ---
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
oled = Screen_UI.init_screen(i2c)

# Rotary Encoder (Pins 18, 19)
r = RotaryIRQ(pin_num_clk=18, pin_num_dt=19, min_val=0, max_val=2,
              reverse=False, range_mode=RotaryIRQ.RANGE_WRAP)

# Buzzer (Pin 27)
buzzer = Pin(27, Pin.OUT)

# MQ-5 Sensor (Pin 34)
mq5_adc = air_sensor.init_sensor(34)

# Alarm Vars
ALARM_HOUR = 16
ALARM_MIN  = 51

# State Vars
cur_temp = 0.0
cur_hum = 0.0
cur_gas = 0
cur_quality = "--"
last_read = 0

def trigger_alarm():
    for _ in range(5):
        buzzer.on(); time.sleep(0.1)
        buzzer.off(); time.sleep(0.1)

# --- STARTUP ---
try:
    oled.text("System Start...", 0, 0)
    oled.show()
except: pass

Clock.connect_wifi()
Clock.sync_time()
print("Ready.")

# --- LOOP ---
while True:
    try:
        # 1. Inputs
        menu_idx = r.value()
        h, m, s, time_str = Clock.get_local_time()

        # 2. Sensors (Every 2s)
        if time.time() - last_read > 2:
            # Temp/Hum
            t, hum = temp_censor.read_dht12(i2c)
            if t is not None:
                cur_temp = t
                cur_hum = hum
            
            # Gas
            raw, qual = air_sensor.read_air_quality(mq5_adc)
            cur_gas = raw
            cur_quality = qual
            
            last_read = time.time()

        # 3. Display
        Screen_UI.draw_interface(oled, menu_idx, time_str, 
                                 cur_temp, cur_hum, 
                                 ALARM_HOUR, ALARM_MIN, 
                                 cur_gas, cur_quality)

        # 4. Alarm
        if h == ALARM_HOUR and m == ALARM_MIN and s == 0:
            trigger_alarm()

        time.sleep(0.1)

    except KeyboardInterrupt:
        break
    except Exception as e:
        print("Error:", e)
        time.sleep(1)
