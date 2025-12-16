import time
import math
import threading

class SensorService:
    def __init__(self, config):
        self.config = config
        self.ads = None
        self.chan_fuel = None
        
        if not self.config['MOCK_HARDWARE']:
            try:
                import board
                import busio
                import adafruit_ads1x15.ads1015 as ADS
                from adafruit_ads1x15.analog_in import AnalogIn
                
                i2c = busio.I2C(board.SCL, board.SDA)
                self.ads = ADS.ADS1015(i2c)
                self.chan_fuel = AnalogIn(self.ads, ADS.P3) # Based on original code
                # Add other channels as needed
            except ImportError:
                 print("Sensor libs not found. Falling back to mock.")
                 self.config['MOCK_HARDWARE'] = True
            except Exception as e:
                 print(f"Sensor init error: {e}. Falling back to mock.")
                 self.config['MOCK_HARDWARE'] = True

    def get_data(self):
        if self.config['MOCK_HARDWARE']:
            return self._mock_data()
        return self._real_data()

    def _mock_data(self):
        # Simulate draining fuel/water and fluctuating battery using sine waves/time
        t = time.time()
        return {
            "fuel": 50 + 40 * math.sin(t / 50),
            "battery": 12.0 + 1.5 * math.sin(t / 20),
            "water": 75 + 20 * math.sin(t / 100),
            "temperature": 20 + 5 * math.sin(t / 200) # Internal temp
        }

    def _real_data(self):
        data = {
            "fuel": 0,
            "battery": 0,
            "water": 0,
             "temperature": 0
        }
        
        # Original Fuel Logic
        if self.chan_fuel:
            try:
                voltage = self.chan_fuel.voltage
                # Calibration from original code:
                # empty = 1.122, full range = 1.842
                percent = (voltage - 1.122) / 1.842 * 100
                data["fuel"] = max(0, min(100, percent)) # Clamp 0-100
            except:
                pass
                
        # Add placeholders for other sensors if wired up
        return data
