from machine import Pin, I2C
import network, ntptime, time
from machine import Pin, PWM
# Buzzer
buzzer = Pin(27, Pin.OUT) 
# Wifi
WIFI_SSID = "UREL-SC661-V-2.4G"
WIFI_PSK  = "TomFryza"
TZ_OFFSET_H = 1
# Alarme parameter
ALARM_HOUR = 16
ALARM_MIN  = 51
ALARM_SECOND = 20
ALARM_DURATION = 6
# Alarme buzzer
def alarm_buzzer(ALARM_DURATION):
    """Fait biper le buzzer actif pendant 'duration' secondes."""
    end_time = time.time() + ALARM_DURATION

    while time.time() < end_time:
        buzzer.on()
        time.sleep(0.1)    # ON 100 ms
        buzzer.off()
        time.sleep(0.1)    # OFF 100 ms

def wifi_connect(timeout=20):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connexion Wi-Fi…")
        wlan.connect(WIFI_SSID, WIFI_PSK)
        t0 = time.ticks_ms()
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), t0) > timeout * 1000:
                raise RuntimeError("Wi-Fi: délai dépassé")
            time.sleep(0.2)
    print("Wi-Fi OK:", wlan.ifconfig())
    return wlan

def sync_ntp():
    print("Sync NTP…")
    ntptime.host = "pool.ntp.org"
    ntptime.settime()
    print("Heure synchronisée !")

def local_time_hms():
    t = time.time() + TZ_OFFSET_H * 3600
    lt = time.localtime(t)
    return lt[3], lt[4], lt[5]

#main
wifi_connect()
sync_ntp()

print("Attente de l’heure de l’alarme...")

triggered = False

try:
    while True:
        h, m, s = local_time_hms()
        print(f"{h:02d}:{m:02d}:{s:02d}", end="\r")

        if h == ALARM_HOUR and m == ALARM_MIN and s == ALARM_SECOND and not triggered:
            alarm_buzzer(ALARM_DURATION)
            triggered = True

        if h != ALARM_HOUR or m != ALARM_MIN or s != ALARM_SECOND:
            triggered = False

        time.sleep(1)

except KeyboardInterrupt:
    led.off()
    print("\nProgramme arrêté.")
