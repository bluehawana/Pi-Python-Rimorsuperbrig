import threading
import time
import random

class GPSService:
    def __init__(self, config):
        self.config = config
        self.latitude = 0.0
        self.longitude = 0.0
        self.speed = 0.0
        self.running = False
        self.lock = threading.Lock()
        
        if not self.config['MOCK_HARDWARE']:
            # Import gps module only if real hardware is expected
            try:
                from gps import gps, WATCH_ENABLE
                self.gpsd = gps(mode=WATCH_ENABLE)
            except ImportError:
                print("GPS module not found. Falling back to mock implementation.")
                self.config['MOCK_HARDWARE'] = True

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._update_loop)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join()

    def _update_loop(self):
        while self.running:
            if self.config['MOCK_HARDWARE']:
                self._mock_update()
            else:
                self._real_update()
            time.sleep(1)

    def _mock_update(self):
        with self.lock:
            # Simulate moving around a central point (London approx)
            self.latitude = 51.5074 + (random.random() - 0.5) * 0.01
            self.longitude = -0.1278 + (random.random() - 0.5) * 0.01
            self.speed = random.uniform(0, 60)

    def _real_update(self):
        try:
             # Basic implementation based on original gpsd.next()
             # In a robust system, we'd handle TPV (Time Position Velocity) reports specifically
             if self.gpsd.waiting(1): # Wait up to 1s for data
                report = self.gpsd.next()
                if report['class'] == 'TPV':
                    with self.lock:
                        self.latitude = getattr(report,'lat',0.0)
                        self.longitude = getattr(report,'lon',0.0)
                        self.speed = getattr(report,'speed',0.0)
        except Exception as e:
            print(f"GPS Error: {e}")

    def get_location(self):
        with self.lock:
            return {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "speed": self.speed
            }
