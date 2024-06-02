import socket
import sys

def alamat(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((server_ip, server_port))
        
        request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(server_ip)
        client_socket.sendall(request.encode())
        
        response = client_socket.recv(4096).decode()
        
        print(response)
    except ConnectionRefusedError:
        print("Koneksi ditolak. Pastikan IP dan Port yang dimasukkan sudah benar.")
    finally:
        client_socket.close()

def input():
    if len(sys.argv) != 3:
        print("Input Tidak lengkap")
        print("Contoh Input : python client.py <server_ip> <server_port>")
        sys.exit(1)
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    return server_ip, server_port

server_ip, server_port = input()
alamat(server_ip, server_port)
