# Deployment Guide (Headless Pi + iPad)

This guide details how to set up the Raspberry Pi 4 as a "Headless Server" that you control via your iPad.

## 1. Prepare the Raspberry Pi (Headless Mode)
1.  **Install OS**: Use **Raspberry Pi OS Lite** (64-bit). You don't need the desktop version since we are using the iPad as the screen.
2.  **Configure Network (Critical)**:
    *   **Scenario A: Central Van Router (Recommended)**: Connect both Starlink and 5G to a central router (like a GL.iNet or Teltonika). Connect Pi and iPad to this *single* Main Van Wi-Fi. This is the most seamless method.
    *   **Scenario B: Multiple Wi-Fi Networks**: You can pre-configure the Pi to connect to *either* the 5G Router or Starlink automatically.
        *   In "Advanced Options" -> "Set username and password", also look for Wi-Fi.
        *   **Pro Tip**: You can add multiple networks by editing `/etc/wpa_supplicant/wpa_supplicant.conf` on the Pi later:
            ```text
            network={
                ssid="Van_5G"
                psk="password"
                priority=2
            }
            network={
                ssid="STARLINK"
                psk="password"
                priority=1
            }
            ```
3.  **Enable SSH & I2C**: Also in "Advanced Options".

## 2. Transfer Files
Since you might not have a screen, use SSH from your Mac to copy files.
```bash
# Copy project (replace 192.168.x.x with Pi's IP)
scp -r /Users/harvadlee/Projects/rferder-py-pi-van pi@192.168.x.x:~/van-computer
```

## 3. Install Dependencies
SSH into the Pi:
```bash
ssh pi@192.168.x.x
cd ~/van-computer
```

Install system libraries:
```bash
sudo apt-get update
sudo apt-get install -y python3-pip gpsd gpsd-clients python3-picamera python3-rpi.gpio i2c-tools
```

Install Python requirements:
```bash
pip3 install -r requirements.txt --break-system-packages
```

## 4. Configuration
1.  **Edit Config**: `cp .env.example .env` then `nano .env`
2.  **Disable Mock Mode**: Set `MOCK_HARDWARE=False`.
3.  **Add API Keys**: Enter your Google Maps and Pushbullet keys.

## 5. Auto-Start on Boot
This is crucial for a headless server.
1.  Create service: `sudo nano /etc/systemd/system/van-computer.service`
2.  Paste content:
    ```ini
    [Unit]
    Description=Van Computer Dashboard
    After=network.target

    [Service]
    User=pi
    WorkingDirectory=/home/pi/van-computer
    ExecStart=/usr/bin/python3 /home/pi/van-computer/app.py
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```
3.  Enable:
    ```bash
    sudo systemctl enable van-computer.service
    sudo systemctl start van-computer.service
    ```

## 6. Accessing on iPad
1.  Ensure iPad is on the same network (Hotspot or Van Wi-Fi).
2.  Open Safari.
3.  Navigate to `http://<pi-ip-address>:5001`.
4.  **Add to Home Screen**: Tap the Share icon -> "Add to Home Screen". This removes the Safari URL bar and gives you a full-screen app experience!
