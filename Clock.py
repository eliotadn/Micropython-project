from machine import Pin, I2C
import network, ntptime, time
# Wifi
WIFI_SSID = "UREL-SC661-V-2.4G"
WIFI_PSK  = "TomFryza"
TZ_OFFSET_H = 1
#Config LED 
led = Pin(2, Pin.OUT)
def blink_led(duration_s=5, interval=0.2):
    end = time.ticks_ms() + int(duration_s * 1000)
    while time.ticks_ms() < end:
        led.on();  time.sleep(interval)
        led.off(); time.sleep(interval)
# Alarme parameter
ALARM_HOUR = 15
ALARM_MIN  = 18
ALARM_SECOND = 00
ALARM_DURATION = 10

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
            blink_led(ALARM_DURATION)
            triggered = True

        if h != ALARM_HOUR or m != ALARM_MIN or s != ALARM_SECOND:
            triggered = False

        time.sleep(1)

except KeyboardInterrupt:
    led.off()
    print("\nProgramme arrêté.")
