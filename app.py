from flask import Flask, render_template, jsonify, request
from config import Config
import os

# Import Services
from services.gps_service import GPSService
from services.sensors import SensorService
from services.notifier import NotifierService
from services.security import SecurityService

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Services
gps_service = GPSService(app.config)
sensor_service = SensorService(app.config)
notifier_service = NotifierService(app.config)
security_service = SecurityService(app.config, notifier_service)

# Start Background Threads
gps_service.start()
security_service.start()

@app.route('/')
def index():
    return render_template('index.html', 
                         maps_api_key=app.config['GOOGLE_MAPS_API_KEY'])

# --- API Endpoints ---

@app.route('/api/status')
def api_status():
    location = gps_service.get_location()
    sensors = sensor_service.get_data()
    security = {
        "armed": security_service.is_armed()
    }
    
    return jsonify({
        "time": os.popen("date").read().strip(), # Quick way to get system time
        "gps": location,
        "sensors": sensors,
        "security": security
    })

@app.route('/api/security/arm', methods=['POST'])
def api_arm_security():
    data = request.json
    if data.get('action') == 'arm':
        security_service.arm()
        return jsonify({"status": "armed"})
    elif data.get('action') == 'disarm':
        security_service.disarm()
        return jsonify({"status": "disarmed"})
    elif data.get('action') == 'test':
        security_service.trigger_test_alarm()
        return jsonify({"status": "test_triggered"})
    return jsonify({"error": "invalid action"}), 400

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "mock_mode": app.config['MOCK_HARDWARE']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
