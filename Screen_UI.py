from sh1106 import SH1106_I2C

def init_screen(i2c):
    # Standard initialization for SH1106 128x64
    try:
        oled = SH1106_I2C(128, 64, i2c)
    except: 
        oled = SH1106_I2C(i2c)
        
    oled.fill(0)
    oled.show()
    return oled

def draw_interface(oled, menu_idx, time_s, temp, hum, al_h, al_m, gas, qual, astros):
    oled.fill(0)
    
    # Mode 0: Current Time Display
    if menu_idx == 0:
        oled.text("CURRENT TIME", 20, 0)
        oled.line(0, 10, 128, 10, 1)
        oled.text(time_s, 25, 30)
        oled.text(f"Alarm: {al_h:02d}:{al_m:02d}", 10, 50)
        
    # Mode 1: Set Alarm Hour
    elif menu_idx == 1:
        oled.text("SET ALARM HOUR", 8, 0)
        oled.line(0, 10, 128, 10, 1)
        oled.text(f"HOUR:", 0, 25)
        oled.text(f"{al_h:02d}", 70, 25)
        oled.text("ROTATE TO CHANGE", 0, 45)
        
    # Mode 2: Set Alarm Minute
    elif menu_idx == 2:
        oled.text("SET ALARM MIN", 12, 0)
        oled.line(0, 10, 128, 10, 1)
        oled.text(f"MIN:", 0, 25)
        oled.text(f"{al_m:02d}", 70, 25)
        oled.text("ROTATE TO CHANGE", 0, 45)

    # Mode 3: ISS Status & Weather/Air Quality
    elif menu_idx == 3:
        oled.text("STATUS", 36, 0)
        oled.line(0, 10, 128, 10, 1)
        
        # ISS Info
        oled.text("Astronauts:", 0, 25)
        oled.text(str(astros), 80, 25)
        
        # Weather / Air Quality Info
        if temp is not None:
            oled.text(f"T: {temp:.1f}C", 0, 45)
            oled.text(f"H: {hum:.1f}%", 70, 45)
        else:
            oled.text("Air Qual: " + str(qual), 0, 45)
            
    # Footer (Page Indicator)
    oled.text("." * (menu_idx + 1), 60, 55)
    oled.show()
