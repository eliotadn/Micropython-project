from machine import Pin, I2C
from rotary_irq import RotaryIRQ
import time
import urequests as requests

# Custom Modules
import temp_censor
import Clock
import Screen_UI
import air_sensor

# --- NOUVEAUX ÉTATS DE PROCESSUS ---
STATE_NAVIGATION = 0    # L'encodeur change le menu
STATE_SET_HOUR = 1      # L'encodeur change ALARM_HOUR
STATE_SET_MINUTE = 2    # L'encodeur change ALARM_MIN

# --- CONFIGURATION ---
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
try:
    oled = Screen_UI.init_screen(i2c)
except Exception as e:
    print(f"OLED initialization error: {e}")
    oled = None 

# Rotary Encoder (Pins 18, 19)
# max_val = 3 pour 4 pages de navigation (0, 1, 2, 3)
r = RotaryIRQ(pin_num_clk=18, pin_num_dt=19, min_val=0, max_val=3,
              reverse=False, range_mode=RotaryIRQ.RANGE_WRAP)
last_r_value = r.value() # Pour la navigation/modification

# NOUVEAU : Bouton Poussoir (Broche de l'encodeur)
BUTTON_PIN = 14 # <<<<<<< CHANGEZ CECI PAR VOTRE BROCHE GPIO RÉELLE
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
last_button_state = button.value()

# Buzzer (Pin 27)
buzzer = Pin(27, Pin.OUT)

# MQ-5 Sensor (Pin 34)
mq5_adc = air_sensor.init_sensor(34)

# Alarm Vars
ALARM_HOUR = 16
ALARM_MIN = 26

# State Vars (CE BLOC DOIT ÊTRE PRÉSENT ET COMPLET)
cur_temp = 0.0      # <-- Définition de cur_temp
cur_hum = 0.0       # <-- Définition de cur_hum
cur_gas = 0         # <-- Définition de cur_gas
cur_quality = "--"  # <-- Définition de cur_quality
last_read = 0

# Variables d'état pour l'ISS
iss_astros = "--" 
last_iss_read = 0
ISS_READ_INTERVAL = 300

# État actuel du processus (Navigation par défaut)
current_process_state = STATE_NAVIGATION 


def trigger_alarm():
    for _ in range(4):
        for _ in range(5):
            buzzer.on(); time.sleep(0.1)
            buzzer.off(); time.sleep(0.1)
        time.sleep(0.2)

def fetch_iss_astros():
    global iss_astros
    try:
        astros_response = requests.get("http://api.open-notify.org/astros.json")
        astros_data = astros_response.json()
        iss_astros = astros_data.get('number', 'Err')
        astros_response.close()
    except Exception as e:
        print("ISS API Error:", e)
        iss_astros = "Err" 
    
    return time.time()

# --- STARTUP ---
try:
    if oled:
        oled.text("System Start...", 0, 0)
        oled.show()
except: pass

Clock.connect_wifi()
Clock.sync_time()
last_iss_read = fetch_iss_astros() 
print("Ready.")

# --- LOOP ---
while True:
    try:
        # 1. Inputs
        new_r_value = r.value()
        new_button_state = button.value()
        h, m, s, time_str = Clock.get_local_time()
        
        # Logique de détection de la rotation
        delta = new_r_value - last_r_value
        if delta == -3: delta = 1
        elif delta == 3: delta = -1

        # ====================================================================
        # A. GESTION DU BOUTON (Transition des états)
        # ====================================================================
        if new_button_state != last_button_state and new_button_state == 0:
            # Le bouton vient d'être pressé (LOW)
            if current_process_state == STATE_NAVIGATION:
                # Clic pour entrer dans le mode réglage (UNIQUEMENT si sur l'écran d'Heure)
                if last_r_value == 0:
                    current_process_state = STATE_SET_HOUR 
            elif current_process_state == STATE_SET_HOUR:
                # Clic pour passer au réglage des minutes
                current_process_state = STATE_SET_MINUTE 
            elif current_process_state == STATE_SET_MINUTE:
                # Clic pour sortir du mode réglage
                current_process_state = STATE_NAVIGATION 
                
        last_button_state = new_button_state
        
        # ====================================================================
        # B. GESTION DE LA ROTATION (Action)
        # ====================================================================

        if current_process_state == STATE_NAVIGATION:
            # En mode navigation, la rotation change le menu_idx
            menu_idx = new_r_value
            last_r_value = new_r_value # Maintient la position de l'encodeur

        elif current_process_state == STATE_SET_HOUR:
            # En mode réglage HEURE, la rotation change ALARM_HOUR
            if delta != 0:
                ALARM_HOUR = (ALARM_HOUR + delta) % 24
            menu_idx = 0 # Affichage de la page de l'heure
            last_r_value = new_r_value
            
        elif current_process_state == STATE_SET_MINUTE:
            # En mode réglage MINUTE, la rotation change ALARM_MIN
            if delta != 0:
                ALARM_MIN = (ALARM_MIN + delta) % 60
            menu_idx = 0 # Affichage de la page de l'heure
            last_r_value = new_r_value
        
        # 2. Sensors (Every 2s) - Utilise last_read et cur_temp/cur_hum/cur_gas/cur_quality
        if time.time() - last_read > 2:
            t, hum = temp_censor.read_dht12(i2c)
            if t is not None:
                cur_temp = t
                cur_hum = hum
                
            raw, qual = air_sensor.read_air_quality(mq5_adc)
            cur_gas = raw
            cur_quality = qual
            
            last_read = time.time()

        # 3. Appel à l'API ISS 
        if current_process_state == STATE_NAVIGATION and new_r_value == 3 and time.time() - last_iss_read > ISS_READ_INTERVAL:
            last_iss_read = fetch_iss_astros()

        # 4. Display 
        if oled:
            # Passage de l'état du processus à Screen_UI
            Screen_UI.draw_interface(oled, last_r_value, current_process_state, time_str, 
                             cur_temp, cur_hum, 
                             ALARM_HOUR, ALARM_MIN, 
                             cur_gas, cur_quality, iss_astros)

        # 5. Alarm (Déclenchement uniquement en mode NAVIGATION, écran 0)
        if current_process_state == STATE_NAVIGATION and last_r_value == 0 and h == ALARM_HOUR and m == ALARM_MIN and s == 0:
            trigger_alarm()

        time.sleep(0.05) # Délai réduit pour une meilleure réactivité

    except KeyboardInterrupt:
        break
    except Exception as e:
        print("Error:", e)
        time.sleep(1)
