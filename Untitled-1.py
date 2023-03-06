import socket

HOST = '192.168.2.123'  # The IP address you want to listen on
PORT = 10012  # The port you want to listen on

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
s.bind((HOST, PORT))

# Listen for incoming connections
s.listen(1)

# Accept incoming connections
conn, addr = s.accept()
print('Connected by', addr)

# Continuously receive incoming data
while True:
    data = conn.recv(1024)  # Buffer size is 1024 bytes
    if not data:
        break
    print('Received data:', data)

# Close the connection
conn.close()