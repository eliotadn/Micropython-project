# Screen_UI.py
from sh1106 import SH1106_I2C

def init_screen(i2c):
    # Initialize screen with provided I2C bus
    oled = SH1106_I2C(128, 64, i2c)
    oled.flip(1) # Flip if needed
    return oled

def draw_interface(oled, menu_index, time_str, temp, hum, alarm_h, alarm_m):
    oled.fill(0) # Clear screen
    
    # --- MENU 0 : TIME ---
    if menu_index == 0:
        oled.text("TIME", 48, 0)
        oled.line(0, 10, 128, 10, 1)
        oled.text(time_str, 25, 30)
        oled.text(f"Alarm: {alarm_h:02d}:{alarm_m:02d}", 10, 50)
    
    # --- MENU 1 : WEATHER ---
    elif menu_index == 1:
        oled.text("WEATHER", 36, 0)
        oled.line(0, 10, 128, 10, 1)
        if temp is not None:
            oled.text(f"Temp: {temp:.1f} C", 0, 25)
            oled.text(f"Hum : {hum:.1f} %", 0, 45)
        else:
            oled.text("Sensor Error", 0, 30)

    # --- MENU 2 : AIR QUALITY ---
    elif menu_index == 2:
        oled.text("AIR QUALITY", 20, 0)
        oled.line(0, 10, 128, 10, 1)
        oled.text("CO2: -- ppm", 0, 30) 
        oled.text("Quality: --", 0, 45)

    # Page indicator (dots at bottom)
    oled.text("." * (menu_index + 1), 60, 55)
    
    oled.show()
