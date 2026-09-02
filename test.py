import socket
import io
from PIL import Image

s = socket.socket()
s.connect(('127.0.0.1', 9091))
s.send(b'screenshot\n')
header = s.recv(1024).decode().strip()
if header.startswith('IMG'):
    size = int(header.split()[1])
    data = b''
    while len(data) < size:
        data += s.recv(4096)
    s.close()
    img = Image.open(io.BytesIO(data))
    img.show()  # This should open the image in your default viewer
    print(f"Image size: {img.size}")
else:
    print("No image received")