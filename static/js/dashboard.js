let map;
let marker;
let securityArmed = false;

// Initialize Map
function initMap() {
    // Default to London if no GPS
    const defaultLocation = { lat: 51.505, lng: -0.09 };
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 13,
        center: defaultLocation,
        styles: [
            { elementType: "geometry", stylers: [{ color: "#242f3e" }] },
            { elementType: "labels.text.stroke", stylers: [{ color: "#242f3e" }] },
            { elementType: "labels.text.fill", stylers: [{ color: "#746855" }] },
            // Add more dark mode styles here for full effect
        ]
    });
    marker = new google.maps.Marker({
        position: defaultLocation,
        map: map,
        title: "Van Location"
    });
}

// Update Dashboard Data
async function updateDashboard() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();

        // Update Clock
        document.getElementById('clock').innerText = new Date().toLocaleTimeString();

        // Update Gauges
        updateGauge('fuel', data.sensors.fuel);
        updateGauge('battery', data.sensors.battery, 15); // Max 15V
        updateGauge('water', data.sensors.water);
        document.getElementById('val-temp').innerText = data.sensors.temperature.toFixed(1) + '°C';

        // Update Map
        if (data.gps.latitude && data.gps.longitude) {
            const newPos = { lat: data.gps.latitude, lng: data.gps.longitude };
            marker.setPosition(newPos);
            map.setCenter(newPos);
        }

        // Update Security Status
        updateSecurityUI(data.security.armed);

    } catch (error) {
        console.error("Error fetching status:", error);
    }
}

function updateGauge(type, value, max = 100) {
    const percentage = Math.min(100, Math.max(0, (value / max) * 100));
    const bar = document.getElementById(`bar-${type}`);
    const valText = document.getElementById(`val-${type}`);

    bar.style.width = `${percentage}%`;
    valText.innerText = type === 'battery' ? `${value.toFixed(1)}V` : `${value.toFixed(0)}%`;

    // Color coding
    if (percentage < 20) {
        bar.style.backgroundColor = '#ff4444';
    } else {
        bar.style.backgroundColor = '#00ff99';
    }
}

function updateSecurityUI(armed) {
    securityArmed = armed;
    const statusDiv = document.getElementById('security-status');
    const btn = document.getElementById('btn-security');

    if (armed) {
        statusDiv.innerText = "SYSTEM ARMED";
        statusDiv.className = "status-indicator status-armed";
        btn.innerText = "DISARM SYSTEM";
        btn.className = "control-btn btn-disarm";
    } else {
        statusDiv.innerText = "SYSTEM DISARMED";
        statusDiv.className = "status-indicator status-safe";
        btn.innerText = "ARM SYSTEM";
        btn.className = "control-btn btn-arm";
    }
}

// Button Handlers
document.getElementById('btn-security').addEventListener('click', async () => {
    const action = securityArmed ? 'disarm' : 'arm';
    await fetch('/api/security/arm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: action })
    });
    updateDashboard(); // Immediate update
});

document.getElementById('btn-test-alarm').addEventListener('click', async () => {
    await fetch('/api/security/arm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'test' })
    });
});

// Voice Control
if ('webkitSpeechRecognition' in window) {
    const recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = false;

    recognition.onstart = () => {
        document.getElementById('voice-status').style.display = 'block';
    };

    recognition.onresult = (event) => {
        const command = event.results[event.results.length - 1][0].transcript.toLowerCase();
        console.log("Voice Command:", command);

        if (command.includes("arm security")) {
            document.getElementById('btn-security').click();
        } else if (command.includes("show map")) {
            // Focus map logic if needed
        }
    };

    // Auto-start for demo purposes (might need interaction first in modern browsers)
    // recognition.start();
}

// Start Polling
setInterval(updateDashboard, 1000); // Update every 1s
window.onload = initMap;
