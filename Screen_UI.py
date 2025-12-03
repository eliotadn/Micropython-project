from sh1106 import SH1106_I2C

def init_screen(i2c):
    try:
        oled = SH1106_I2C(128, 64, i2c)
    except: 
        oled = SH1106_I2C(i2c)
        
    oled.fill(0)
    oled.show()
    return oled

# Définition des états pour Screen_UI (doit correspondre à main.py)
STATE_NAVIGATION = 0    
STATE_SET_HOUR = 1      
STATE_SET_MINUTE = 2    

# Ajout de 'state' dans les arguments
def draw_interface(oled, menu_idx, state, time_s, temp, hum, al_h, al_m, gas, qual, astros):
    oled.fill(0)
    
    # --- ÉCRANS DE RÉGLAGE (Priorité haute) ---
    if state == STATE_SET_HOUR:
        oled.text("SET ALARM", 20, 0)
        oled.line(0, 10, 128, 10, 1)
        oled.text(f"HOUR: {al_h:02d} <", 0, 25) # Indicateur visuel
        oled.text(f"MIN:  {al_m:02d}", 0, 40)
        oled.text("PRESS to set minutes", 0, 55)
        
    elif state == STATE_SET_MINUTE:
        oled.text("SET ALARM", 20, 0)
        oled.line(0, 10, 128, 10, 1)
        oled.text(f"HOUR: {al_h:02d}", 0, 25)
        oled.text(f"MIN:  {al_m:02d} <", 0, 40) # Indicateur visuel
        oled.text("PRESS to finish", 0, 55)
    
    # --- ÉCRANS DE NAVIGATION (Si l'état est STATE_NAVIGATION) ---
    elif state == STATE_NAVIGATION:
        
        # Mode 0: Affichage de l'heure
        if menu_idx == 0:
            oled.text("CURRENT TIME", 20, 0)
            oled.line(0, 10, 128, 10, 1)
            oled.text(time_s, 25, 30)
            oled.text(f"Alarm: {al_h:02d}:{al_m:02d}", 10, 50)
            
        # Mode 1: Météo
        elif menu_idx == 1:
            oled.text("WEATHER", 36, 0)
            oled.line(0, 10, 128, 10, 1)
            if temp is not None:
                oled.text(f"T: {temp:.1f}C", 0, 25)
                oled.text(f"H: {hum:.1f}%", 0, 45)
            else:
                oled.text("Sensor Error", 0, 30)
            
        # Mode 2: Qualité de l'Air
        elif menu_idx == 2:
            oled.text("AIR QUALITY", 20, 0)
            oled.line(0, 10, 128, 10, 1)
            oled.text(f"Gas: {gas}", 0, 25)
            oled.text(f"Qual: {qual}", 0, 45)

        # Mode 3: ISS Status & Météo/Air Qualité
        elif menu_idx == 3:
            oled.text("STATUS", 36, 0)
            oled.line(0, 10, 128, 10, 1)
            oled.text("Astronauts:", 0, 25)
            oled.text(str(astros), 80, 25)
            oled.text("T:" + str(cur_temp), 0, 45)
            
        # Footer (Indicateur de page UNIQUEMENT si en mode NAVIGATION)
        oled.text("." * (menu_idx + 1), 60, 55)
        
    oled.show()
