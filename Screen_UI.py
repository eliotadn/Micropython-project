from sh1106 import SH1106_I2C

def init_screen(i2c):
    # --- CORRECTION INIT ---
    # Tente d'initialiser en passant l'objet i2c en premier (standard pour sh1106)
    try:
        oled = SH1106_I2C(128, 64, i2c)
    except TypeError:
        # Si ça échoue, on tente la version simplifiée sans dimensions
        oled = SH1106_I2C(i2c)
    except Exception:
        # Dernière tentative : i2c, largeur, hauteur
        oled = SH1106_I2C(i2c, 128, 64)

    # --- CORRECTION FLIP ---
    # La ligne oled.flip(1) a été supprimée car elle n'existe pas.
    
    # SI L'ÉCRAN EST À L'ENVERS : Décommentez les 2 lignes ci-dessous :
    # oled.write_cmd(0xC8) 
    # oled.write_cmd(0xA1)
    
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
