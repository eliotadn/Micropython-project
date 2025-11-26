import network
import ntptime
import time

# EDIT YOUR WIFI HERE
SSID = "UREL-SC661-V-2.4G"
PASS  = "TomFryza"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(SSID, PASS)
        while not wlan.isconnected():
            time.sleep(1)

def sync_time():
    try:
        ntptime.settime()
    except:
        pass

def get_local_time():
    # GMT+1 adjustment (add 3600 seconds)
    t = time.localtime(time.time() + 3600)
    return t[3], t[4], t[5], "{:02d}:{:02d}:{:02d}".format(t[3], t[4], t[5])
