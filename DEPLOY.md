# Deployment Guide (Headless Pi + iPad)

This guide details how to set up the Raspberry Pi 4 as a "Headless Server" that you control via your iPad.

## 1. Prepare the Raspberry Pi (Headless Mode)
1.  **Install OS**: Use **Raspberry Pi OS Lite** (64-bit). You don't need the desktop version since we are using the iPad as the screen.
2.  **Configure Network (Critical)**:
    *   **Option A (Mobile Hotspot)**: Configure the Pi to connect to your iPhone/iPad's Personal Hotspot.
    *   **Option B (Van Wi-Fi)**: If you have a router in the van, connect both Pi and iPad to it.
    *   *Tip: Set these up in the Raspberry Pi Imager "Advanced Options" (Ctrl+Shift+X) before writing to the SD card.*
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
