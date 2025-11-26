import network
import ntptime
import time

WIFI_SSID = "UREL-SC661-V-2.4G"
WIFI_PSK  = "TomFryza"
TZ_OFFSET_H = 1  # Time zone offset

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PSK)
        start = time.time()
        while not wlan.isconnected():
            if time.time() - start > 20:
                print("WiFi connection failed")
                return False
            time.sleep(0.5)
    print("WiFi connected:", wlan.ifconfig())
    return True

def sync_time():
    try:
        ntptime.host = "pool.ntp.org"
        ntptime.settime()
        print("Time synchronized")
    except:
        print("NTP sync error")

def get_local_time():
    """Returns (HH, MM, SS, 'HH:MM:SS')"""
    t = time.time() + TZ_OFFSET_H * 3600
    lt = time.localtime(t)
    h, m, s = lt[3], lt[4], lt[5]
    time_str = "{:02d}:{:02d}:{:02d}".format(h, m, s)
    return h, m, s, time_str

