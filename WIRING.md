# Hardware Wiring Guide

This guide details how to connect the sensors to the Raspberry Pi 4 for the Van Computer.

## Components Needed
1.  **Raspberry Pi 4**
2.  **ADS1115 ADC Module** (for Analog sensors)
3.  **NEO-6M GPS Module** (or similar USB/UART GPS)
4.  **PIR Motion Sensor** (HC-SR501)
5.  **Pi Camera Module**
6.  **Simulated Analog Sensors**:
    *   Potentiometers can simulate Fuel/Water levels for testing.
    *   Voltage dividers are needed for 12V Battery monitoring.

## 1. ADS1115 (Analog to Digital Converter)
Connects via I2C.

| ADS1115 Pin | Raspberry Pi Pin |
| :--- | :--- |
| VDD | 3.3V (Pin 1) |
| GND | GND (Pin 9) |
| SCL | GPIO 3 (SCL) (Pin 5) |
| SDA | GPIO 2 (SDA) (Pin 3) |

**Sensor Inputs:**
*   **A0**: Fuel Level Sender
*   **A1**: Battery Voltage (Must use voltage divider to drop 12V to <3.3V!)
*   **A2**: Water Level Sender
*   **A3**: Spare

> [!WARNING]
> **Battery Monitoring**: Do NOT connect the 12V car battery directly to the ADS1115 or Pi. You MUST use a voltage divider (e.g., 10kΩ and 2.2kΩ resistors) to scale 12V down to a safe range (approx 2V).

## 2. GPS Module (NEO-6M)
Connects via UART (Serial).

| GPS Pin | Raspberry Pi Pin |
| :--- | :--- |
| VCC | 3.3V or 5V (Check module specs) |
| GND | GND |
| TX | GPIO 15 (RXD) (Pin 10) |
| RX | GPIO 14 (TXD) (Pin 8) |

*Note: You may need to enable default serial port in `raspi-config`.*

## 3. PIR Motion Sensor
Connects via GPIO.

| PIR Pin | Raspberry Pi Pin |
| :--- | :--- |
| VCC | 5V (Pin 2) |
| SUB | GND (Pin 6) |
| OUT | GPIO 17 (Pin 11) *Configurable in config.py* |

## 4. Pi Camera
Connects to the CSI camera port on the Raspberry Pi board using the ribbon cable.
*   Enable camera interface in `raspi-config`.

## Powering the Pi in a Van
*   Use a high-quality **12V to 5V (USB-C)** buck converter / hardwire kit.
*   Ensure it provides at least 3A.
*   Ideally, connect to the "Leisure Battery" to avoid draining the starter battery.
