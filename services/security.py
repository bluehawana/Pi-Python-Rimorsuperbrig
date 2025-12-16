import time
import threading
import os
from datetime import datetime

class SecurityService:
    def __init__(self, config, notifier):
        self.config = config
        self.notifier = notifier
        self.armed = False
        self.running = True
        self.last_motion_time = 0
        self.thread = threading.Thread(target=self._monitor_loop)
        self.thread.daemon = True
        
        self.output_dir = os.path.join(os.getcwd(), 'static', 'captures')
        os.makedirs(self.output_dir, exist_ok=True)

        if not self.config['MOCK_HARDWARE']:
             try:
                 import RPi.GPIO as GPIO
                 import picamera
                 GPIO.setmode(GPIO.BCM)
                 GPIO.setup(self.config['PIN_PIR'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
             except ImportError:
                 print("Security libs not found. Falling back to mock.")
                 self.config['MOCK_HARDWARE'] = True

    def start(self):
        self.thread.start()

    def arm(self):
        self.armed = True
        return True

    def disarm(self):
        self.armed = False
        return True
    
    def is_armed(self):
        return self.armed

    def _monitor_loop(self):
        while self.running:
            if self.armed:
                motion_detected = False
                
                if self.config['MOCK_HARDWARE']:
                    # No automatic random motion in mock mode to avoid spamming logic
                    # We can trigger it manually via API if needed
                    pass 
                else:
                    import RPi.GPIO as GPIO
                    if GPIO.input(self.config['PIN_PIR']):
                         motion_detected = True

                if motion_detected:
                     current_time = time.time()
                     if current_time - self.last_motion_time > 30: # Cooldown
                         self.last_motion_time = current_time
                         self._handle_intrusion()
            
            time.sleep(0.5)

    def _handle_intrusion(self):
        print("Intrusion Detected!")
        filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        filepath = os.path.join(self.output_dir, filename)
        
        # Capture Image
        if self.config['MOCK_HARDWARE']:
             # Create dummy file
             with open(filepath, 'w') as f:
                 f.write("Mock Image Data")
        else:
            import picamera
            with picamera.PiCamera() as camera:
                camera.rotation = 180
                camera.capture(filepath)
        
        # Notify
        self.notifier.send_push("Security Alert", "Motion detected in van!")
        self.notifier.send_email("Security Alert: Motion Detected", "Motion detected.", filepath)

    # For manual testing
    def trigger_test_alarm(self):
        self._handle_intrusion()
