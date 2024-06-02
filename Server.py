from socket import *
import threading

# Port dan Alamat server
PORT = 12345
SERVER = gethostbyname(gethostname())
ADDR = (SERVER, PORT)

# Objek socket menggunakan IPv4 dan TCP
server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)

def Handle_Request(msg):

    headers = msg.split('\n')
    filename = headers[0].split()[1]

    if filename == '/':
        filename = '/index.html'

    try:
        with open(f".{filename}", "r") as file:
            content = file.read()
        response = "HTTP/1.1 200 OK\n\n" + content
    except FileNotFoundError:
        response = "HTTP/1.1 404 Not Found\n\nFile Not Found!"

    return response

def handle_Client(connectionSocket, adr):

    print(f"Koneksi Baru, {adr} Terhubung!")
    connected = True
    while connected:
        msg = connectionSocket.recv(1024).decode()
        if msg:
            content = Handle_Request(msg)
            connectionSocket.sendall(content.encode())
            connected = False
    connectionSocket.close()

def start():

    server.listen()
    print(f"Alamat Server : {SERVER}:{PORT}")
    print(f"Server listening...")
    while True:
        connectionSocket, adr = server.accept()
        thread = threading.Thread(target=handle_Client, args=(connectionSocket, adr))
        thread.start()
        print(f"Koneksi sedang aktif....")

print("Server dimulai...")
start()
