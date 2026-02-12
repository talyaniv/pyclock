# HDMI Analog Clock (Raspberry Pi / macOS Preview)

## A minimal black-and-white analog clock designed for HDMI display.

### Features
	•	Smooth analog clock rendering
	•	Hour / minute / seconds hands
	•	Date display with rounded outline
	•	Logo image (semi-transparent)
	•	Live temperature from internet
	•	Looping 60 BPM background audio synced to seconds
	•	Works on Raspberry Pi Zero W and macOS preview

---

### 1️⃣ Requirements

Hardware (target device)
	•	Raspberry Pi Zero W
	•	HDMI display
	•	Internet connection (for time sync + weather)
	•	Speakers (optional, for audio)

Software
	•	Python 3.9+
	•	pip
	•	virtual environment support

---

### 2️⃣ Project Structure

```
clock.py
brand_logo.png
background.wav
README.md
```

---

### 3️⃣ Installation — macOS (Preview Environment)

If you encountered the externally-managed-environment error on macOS (Homebrew Python), use a virtual environment.

Create virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies

```
pip install pygame requests
```

Run preview

```
python clock.py
```

A windowed preview will appear (640×480).

---

## 34️⃣ Installation — Raspberry Pi Zero W

Recommended OS:
	•	Raspberry Pi OS Lite
	•	Raspberry Pi OS with Desktop

Update system

```
sudo apt update
sudo apt upgrade -y
```

Install system packages
```
sudo apt install -y python3 python3-venv python3-pip \
libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```
These packages are required for pygame graphics and audio.

---

Create project folder

```
mkdir ~/hdmi-clock
cd ~/hdmi-clock
```
Copy project files into this folder.

---

Create virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
```

Install Python dependencies

```
pip install pygame requests
```
---

### 5️⃣ Run the Clock

```
python clock.py
```

To run full screen on HDMI, configure fullscreen mode inside the script.

---

# 6️⃣ Enable Automatic Time Sync (Important)

Raspberry Pi uses NTP for:
	•	Accurate time
	•	Daylight saving adjustment
	•	Correct timezone

Verify status:

```
timedatectl
```

Enable if needed:
```
sudo timedatectl set-ntp true
```

Set timezone (example: Israel):
```
sudo timedatectl set-timezone Asia/Jerusalem
```
This ensures your 60 BPM audio remains synchronized with real time.

---

### 7️⃣ Autostart on Boot (Optional)

Configure the Pi to behave like a dedicated clock appliance.

Create service file
```
sudo nano /etc/systemd/system/hdmi-clock.service
```

Paste:
```
[Unit]
Description=HDMI Clock
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/hdmi-clock
ExecStart=/home/pi/hdmi-clock/.venv/bin/python clock.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```
sudo systemctl daemon-reexec
sudo systemctl enable hdmi-clock
sudo systemctl start hdmi-clock
```

---

### 8️⃣ Audio Notes
	•	.wav recommended for Raspberry Pi Zero performance
	•	Audio starts synced to the first second tick
	•	Volume controlled inside the script

---

### 9️⃣ Troubleshooting

pygame fails to install on Pi

Ensure SDL packages were installed before running pip install.

No temperature displayed

Check internet connection.

No sound

Run:

```
alsamixer
```

Script works on one Mac but not another

Always use a virtual environment when using Homebrew Python.
