# Deployment Guide

Follow these steps to deploy the code from your computer to the Raspberry Pi 4.

## 1. Prepare the Raspberry Pi
1.  **Install OS**: Install Raspberry Pi OS (Legacy or Desktop) on your SD card.
2.  **Enable Interfaces**:
    *   Run `sudo raspi-config`
    *   Interface Options -> SSH (Enable)
    *   Interface Options -> I2C (Enable)
    *   Interface Options -> Camera (Enable)
    *   Interface Options -> Serial Port (Enable shell messages: No, Enable hardware port: Yes)
3.  **Connect Network**: Ensure Pi is on the same Wi-Fi as your computer.

## 2. Transfer Files
On your Mac (this computer), open a terminal and copy the project files to the Pi.
Replace `pi@raspberrypi.local` with your Pi's actual user/hostname.

```bash
# Copy the entire project folder
scp -r /Users/harvadlee/Projects/rferder-py-pi-van pi@raspberrypi.local:~/van-computer
```

## 3. Install Dependencies on Pi
SSH into the Pi:
```bash
ssh pi@raspberrypi.local
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
1.  **Edit Config**:
    ```bash
    cp .env.example .env
    nano .env
    ```
2.  **Disable Mock Mode**:
    Change `MOCK_HARDWARE=True` to `MOCK_HARDWARE=False`.
3.  **Add API Keys**: Enter your Google Maps and Pushbullet keys.

## 5. Run the Application
Test it manually first:
```bash
python3 app.py
```
Visit `http://<pi-ip-address>:5000` in your browser.

## 6. Auto-Start on Boot (Optional)
Create a systemd service to make it run automatically when the van starts.

1.  Create service file:
    ```bash
    sudo nano /etc/systemd/system/van-computer.service
    ```

2.  Paste this content (adjust paths if needed):
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

3.  Enable and start:
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable van-computer.service
    sudo systemctl start van-computer.service
    ```
