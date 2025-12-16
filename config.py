import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MOCK_HARDWARE = os.getenv('MOCK_HARDWARE', 'True').lower() == 'true'
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')
    
    EMAIL_SENDER = os.getenv('EMAIL_SENDER', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER', '')
    
    PUSHBULLET_API_KEY = os.getenv('PUSHBULLET_API_KEY', '')
    
    # Hardware Pins (BCM numbering)
    PIN_PIR = 17      # Was 11 in BOARD -> ~17 in BCM (Check physical pinout)
    PIN_ALARM_IN = 22 # Was 15 in BOARD -> ~22 in BCM
    
    # ADC Channels
    CHAN_FUEL = 0
    CHAN_BATTERY = 1
    CHAN_WATER = 2
