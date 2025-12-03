from machine import ADC, Pin

def init_sensor(pin_num):
    # ADC Initialization
    adc = ADC(Pin(pin_num))
    adc.atten(ADC.ATTN_11DB) # Full range 3.3V
    adc.width(ADC.WIDTH_12BIT)
    return adc

def read_air_quality(adc):
    raw = adc.read()
    
    # Basic Thresholds for MQ-5 (These may require real-world calibration)
    quality = "Good"
    if raw > 1500:
        quality = "Moderate"
    if raw > 2500:
        quality = "Bad"
        
    return raw, quality
