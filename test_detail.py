import socket

s = socket.socket()
s.connect(('127.0.0.1', 9091))
s.send(b'screenshot\n')
raw_header = s.recv(1024)
# Remove UTF-8 BOM if present (0xEF,0xBB,0xBF)
if raw_header.startswith(b'\xef\xbb\xbf'):
    raw_header = raw_header[3:]  # strip BOM
    print("Stripped BOM")
print(f"Raw header bytes: {raw_header}")
try:
    header = raw_header.decode().strip()
except UnicodeDecodeError:
    header = raw_header.decode('utf-8', errors='ignore').strip()
print(f"Decoded header: '{header}'")
if header.startswith('IMG'):
    size = int(header.split()[1])
    print(f"Image size: {size}")
    data = b''
    while len(data) < size:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
    print(f"Received {len(data)} bytes")
    s.close()
    if len(data) == size:
        with open('C:\\RAT_Client\\test_output.jpg', 'wb') as f:
            f.write(data)
        print("Saved as test_output.jpg")
    else:
        print(f"Incomplete: expected {size}, got {len(data)}")
else:
    print("No IMG header")
s.close()