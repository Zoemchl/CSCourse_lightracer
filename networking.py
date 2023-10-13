import socket
import json 


def create_socket_server(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    s.settimeout(5)
    return s

def create_socket_client(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.settimeout(5)
    return s

def send_object(sock, obj):
    data = json.dumps(obj)
    sock.sendall(data.encode())

def receive_object(sock, buffer_size=1024, timeout=None):
    sock.settimeout(timeout)
    try:
        data = sock.recv(buffer_size).decode()
        return json.loads(data)
    except Exception as e:
        print(f"Error receiving data: {e}")
        return None

