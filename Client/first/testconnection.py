import socket

def send_message(sock, message):
    sock.sendall(message.encode())

def receive_message(sock, buffer_size=1024):
    data = sock.recv(buffer_size)
    return data.decode()

def main():
    host = 'localhost'  # Change this to the server's IP address
    port = 6066        # Change this to the server's port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        
        # Send a message to the server
        message_to_send = "Hello, server!\n"
        send_message(sock, message_to_send)
        
        # Receive a response from the server
        response = receive_message(sock)
        print("Server response:", response)

if __name__ == "__main__":
    main()
