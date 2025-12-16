# Raspberry Pi Van Computer (Rimor Superbrig 747)

A comprehensive car computer system designed for Vanlife in Europe. This system runs on a Raspberry Pi 4 and provides a web-based dashboard for vehicle monitoring, security, and navigation.

## Features
- **Headless Architecture**: Designed to run on a hidden Pi 4, controlled via an iPad Mini or smartphone.
- **Vehicle Monitoring**: Real-time gauges for Fuel, Leisure Battery, and Water levels (via ADS1115).
- **Security System**: PIR motion detection with Pi Camera image capture and Pushbullet/Email alerts.
- **Navigation**: Integrated Google Maps tracking with GPS location.
- **Voice Control**: Hands-free voice commands.
- **Network Resilience**: Configured for failover between 5G Router and Starlink Mini.

## Hardware Setup
- **Server**: Raspberry Pi 4 (Headless)
- **Client/Display**: iPad Mini 5G (or any tablet/phone)
- **Power**: Supercapacitor UPS (for safe shutdown in heat)
- **Connectivity**: 5G Router + Starlink Mini

## Documentation
*   [Deployment Guide (DEPLOY.md)](DEPLOY.md) - How to install and run the software.
*   [Wiring Guide (WIRING.md)](WIRING.md) - How to connect sensors and power.

## Credits & Acknowledgements
This project continues the work and inspiration from:
*   **Rupert Ferder** ([@rupertferder6768](https://www.youtube.com/@rupertferder6768)) - Mentor and provider of the original codebase foundation.
*   **Original Inspiration**: Based on concepts from the [Pekaway/VAN_PI](https://github.com/Pekaway/VAN_PI) repository.

## License
MIT
