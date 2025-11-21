# OpenBMC CI/CD Pipeline

This repository contains Jenkins pipeline for automated testing of OpenBMC.

## Pipeline Stages

1. **Start QEMU with OpenBMC** - Launches OpenBMC in QEMU emulator
2. **Redfish API Tests** - Runs automated API tests using Redfish interface
3. **WebUI Tests** - Executes Selenium-based web interface tests
4. **Load Testing** - Performs load testing using Locust

## Requirements

- Jenkins with Docker support
- Python 3.8+
- QEMU system emulator
- Chrome browser (for WebUI tests)