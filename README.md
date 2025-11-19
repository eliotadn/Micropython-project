
# Project Title

A brief description of what this project does and who it's for


## Demo

Insert gif or link to demo


## Deployment

To deploy this project run

| Fonction | Pin ESP32 (FireBeetle) | Écran OLED (I2C) | Horloge RTC (DS3231) | Rotary Encoder |
| :--- | :--- | :--- | :--- | :--- |
| **SDA (Données)** | **GPIO 21** (Violet) | SDA | SDA | - |
| **SCL (Horloge)** | **GPIO 22** (Violet) | SCK ou SCL | SCL | - |
| **Alim (+)** | **3V3** (Rouge) | VCC | VCC | **+** |
| **Masse (-)** | **GND** (Noir) | GND | GND | **GND** |
| **Rotary A** | **GPIO 18** (Jaune) | - | - | **CLK** |
| **Rotary B** | **GPIO 19** (Jaune) | - | - | **DT** |
| **Bouton** | **GPIO 4** (Vert) | - | - | **SW** |
| **LED Alarme** | **GPIO 2 / D9** | - | - | - |
| *Non connecté* | - | - | 32K, SQW | - |

```bash
  npm run deploy
```

![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/th5xamgrr6se0x5ro4g6.png)

