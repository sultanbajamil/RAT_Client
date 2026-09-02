# 🖥️ RAT_Client: Remote Desktop & Input Control Client

**RAT_Client** is a lightweight desktop client developed in Python using **Tkinter** and **Pillow**. It connects to a running **StealthRAT** instance to stream the remote desktop in near real-time and forward mouse movements, clicks, and keystrokes over raw TCP sockets.

---

## 📁 Repository Contents

```text
RAT_Client/
├── remote_client.py   # Primary GUI remote desktop client (Tkinter + Pillow)
├── test.py            # Diagnostic script to capture and display a single frame
├── test_detail.py     # In-depth diagnostic script verifying headers & byte streams
├── Program.cs         # C# client reference interface
├── .gitignore         # Build and cache exclusion patterns
└── README.md          # Project documentation
```

---

## 🌟 Features

- **Live Desktop View**: Continuously requests and renders desktop frames with a configurable refresh interval (`REFRESH_MS`).
- **Input Forwarding**:
  - Translates mouse canvas coordinates to remote desktop dimensions.
  - Supports left, right, and double clicks.
  - Forwards keyboard events and keypress commands.
- **Header & BOM Sanitization**: Automatically strips UTF-8 Byte Order Marks (BOM) from the incoming socket stream to maintain image parsing integrity.
- **Diagnostic Utilities**: Includes standalone test scripts to verify raw network packet arrival, port responsiveness, and JPEG rendering independently of the main GUI.

---

## 🚀 Installation & Running

### Prerequisites
- Python 3.8 or higher.
- Install the required Pillow library:
  ```bash
  pip install pillow
  ```

### Configuration
Open `remote_client.py` and configure your target endpoint:
```python
# === CONFIGURATION ===
TARGET_IP = "192.168.1.100"   # IP address of the target machine running StealthRAT
CMD_PORT = 9090              # Port for command execution & input forwarding
SCREEN_PORT = 9091           # Port for real-time JPEG screen capture streaming
REFRESH_MS = 150             # Refresh delay in milliseconds between frames
```

### Launching the Client
1. Start the client:
   ```bash
   python remote_client.py
   ```
2. A graphical window will open displaying the remote screen. You can interact directly with the canvas to send mouse and keyboard commands.

### Running Diagnostics
If you encounter network connectivity or stream issues, run the diagnostic script:
```bash
python test_detail.py
```
This script validates socket connections to port `9091`, prints header byte analysis, and saves a test capture to `test_output.jpg`.

---

## ⚠️ Disclaimer
This tool is intended exclusively for authorized network auditing, technical education, and laboratory testing. Unauthorized remote access is illegal.
