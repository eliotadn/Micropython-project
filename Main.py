from machine import Pin, I2C
from rotary_irq import RotaryIRQ
import time

# --- CORRECTION DES IMPORTS (Plus de .py) ---
import temp_censor
import Clock
import Screen_UI

# --- HARDWARE CONFIGURATION ---
# 1. I2C (Shared by screen and sensor)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)

# 2. Initialize modules
oled = Screen_UI.init_screen(i2c)

# 3. Rotary Encoder
r = RotaryIRQ(pin_num_clk=18, pin_num_dt=19, min_val=0, max_val=2,
              reverse=False, range_mode=RotaryIRQ.RANGE_WRAP)

# 4. Buzzer
buzzer = Pin(27, Pin.OUT)

# --- ALARM SETTINGS ---
ALARM_HOUR = 15
ALARM_MIN  = 43
alarm_active = False

def trigger_alarm():
    # Short beeps
    for _ in range(5):
        buzzer.on(); time.sleep(0.1)
        buzzer.off(); time.sleep(0.1)

# --- STARTUP ---
# On utilise un try/except pour l'affichage initial au cas où l'écran n'est pas prêt
try:
    oled.text("Connecting...", 0, 0)
    oled.show()
except Exception as e:
    print("Screen warning:", e)

Clock.connect_wifi()
Clock.sync_time()

prev_val = -1
last_sensor_read = 0
cur_temp = 0.0
cur_hum = 0.0

print("System ready.")

# --- MAIN LOOP ---
while True:
    try:
        # 1. Menu handling
        menu_index = r.value()
        
        # 2. Time handling
        h, m, s, time_str = Clock.get_local_time()
        
        # 3. Sensor reading (every 2s)
        if time.time() - last_sensor_read > 2:
            # Note: Assurez-vous que temp_censor a bien une fonction read_dht12
            t, hum = temp_censor.read_dht12(i2c)
            if t is not None:
                cur_temp = t
                cur_hum = hum
            last_sensor_read = time.time()

        # 4. Display update
        Screen_UI.draw_interface(oled, menu_index, time_str, cur_temp, cur_hum, ALARM_HOUR, ALARM_MIN)
        
        # 5. Alarm check
        if h == ALARM_HOUR and m == ALARM_MIN and s == 0:
            trigger_alarm()

        time.sleep(0.1) 
        
    except KeyboardInterrupt:
        print("Stopped.")
        break
    except Exception as e:
        print("Error in loop:", e)
        time.sleep(1) # Pause pour éviter de spammer l'erreur
