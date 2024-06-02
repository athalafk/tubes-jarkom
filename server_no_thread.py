from socket import *

server_ip = gethostbyname(gethostname())
server_port = 12345
address = (server_ip, server_port)

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
            break
    socket.close()

def start():
    server.listen()
    print("Server dimulai...")
    print(f"Alamat Server : {server_ip}:{server_port}")
    print("Server listening...")
    while True:
        socket, addr = server.accept()
        handle_Client(socket, addr)
        print(f"Koneksi dari {addr} telah selesai.")
start()
