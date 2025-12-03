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
        print(f"Connecting to {SSID}...")
        wlan.connect(SSID, PASS)
        # Connection Timeout
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
        if wlan.isconnected():
            print("WiFi Connected.")
        else:
            print("WiFi connection failed.")
            
def sync_time():
    try:
        ntptime.settime()
        print("Time synced via NTP.")
    except Exception as e:
        print(f"NTP sync failed: {e}")
        pass

def get_local_time():
    # GMT+1 adjustment (adjust if your timezone changes)
    # The current UTC time is adjusted by 3600 seconds for GMT+1
    t = time.localtime(time.time() + 3600) 
    # Returns: hour, minute, second, formatted_string
    return t[3], t[4], t[5], "{:02d}:{:02d}:{:02d}".format(t[3], t[4], t[5])
