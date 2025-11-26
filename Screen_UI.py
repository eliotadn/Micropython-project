from sh1106 import SH1106_I2C

def init_screen(i2c):
    try:
        oled = SH1106_I2C(i2c)
    except:
        oled = SH1106_I2C(128, 64, i2c)
        
    # Rotate if needed (Uncomment if upside down)
    # oled.write_cmd(0xC8) 
    # oled.write_cmd(0xA1)
    
    return oled

def draw_interface(oled, menu, time_s, temp, hum, al_h, al_m, gas, qual):
    oled.fill(0)
    
    # Page 1: Time
    if menu == 0:
        oled.text("TIME", 48, 0)
        oled.line(0, 10, 128, 10, 1)
        oled.text(time_s, 25, 30)
        oled.text(f"Alarm: {al_h:02d}:{al_m:02d}", 10, 50)
    
    # Page 2: Weather
    elif menu == 1:
        oled.text("WEATHER", 36, 0)
        oled.line(0, 10, 128, 10, 1)
        if temp is not None:
            oled.text(f"T: {temp:.1f}C", 0, 25)
            oled.text(f"H: {hum:.1f}%", 0, 45)
        else:
            oled.text("Sensor Error", 0, 30)

    # Page 3: Air Quality
    elif menu == 2:
        oled.text("AIR QUALITY", 20, 0)
        oled.line(0, 10, 128, 10, 1)
        oled.text(f"Gas: {gas}", 0, 25)
        oled.text(f"Qual: {qual}", 0, 45)

    # Footer
    oled.text("." * (menu + 1), 60, 55)
    oled.show()
