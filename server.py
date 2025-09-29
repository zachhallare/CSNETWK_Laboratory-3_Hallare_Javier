import socket
import threading
import random

HOST = "127.0.0.1"  # localhost
PORT = 5050         
SERVER_NAME = "Server of mga Pogi"  # replace with your name

QUIT = False

class ClientThread(threading.Thread):
    def __init__(self, client_socket, addr):
        super().__init__()
        self.client_socket = client_socket
        self.addr = addr

    def run(self):
        global QUIT
        try:
            # Receive data from client
            data = self.client_socket.recv(1024).decode()
            if not data:
                return
            client_name, client_number_str = data.split(',')
            client_number = int(client_number_str)

            # Display info
            print(f"Received from client: {client_name.strip()} with number {client_number}")
            print(f"{SERVER_NAME} is handling the connection.")

            # Server picks a number
            server_number = random.randint(1, 100)
            print(f"Server number: {server_number}, sum: {client_number + server_number}")

            # Send server info back to client
            response = f"{SERVER_NAME},{server_number}"
            self.client_socket.sendall(response.encode())

            # Terminate server if number out of range
            if not (1 <= client_number <= 100):
                print("Client sent number out of range. Shutting down server.")
                QUIT = True
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.client_socket.close()

def main():
    global QUIT
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"{SERVER_NAME} listening on {HOST}:{PORT}")

    while not QUIT:
        try:
            server_socket.settimeout(1)
            client_sock, addr = server_socket.accept()
            thread = ClientThread(client_sock, addr)
            thread.start()
        except socket.timeout:
            continue
        except KeyboardInterrupt:
            print("Server interrupted by user.")
            break

    server_socket.close()
    print("Server terminated.")

if __name__ == "__main__":
    main()
