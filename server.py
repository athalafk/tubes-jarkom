from socket import *
import threading

ip = gethostbyname(gethostname())
port = 12345
address = (ip, port)

server = socket(AF_INET, SOCK_STREAM)
server.bind(address)

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

def handle_Client(socket, addr):
    print(f"Koneksi Baru, {addr} Terhubung!")
    while True:
        msg = socket.recv(1024).decode()
        if msg:
            content = Handle_Request(msg)
            socket.sendall(content.encode())
    socket.close()

def start():
    server.listen()
    print("Server dimulai...")
    print(f"Alamat Server : {ip}:{port}")
    print(f"Server listening...")
    while True:
        socket, addr = server.accept()
        thread = threading.Thread(target=handle_Client, args=(socket, addr))
        thread.start()
        print(f"Koneksi sedang aktif....")

start()
