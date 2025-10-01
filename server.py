import socket
import threading
import random

HOST = "192.168.0.88"  # localhost
PORT = 5050         
SERVER_NAME = "Server of mga Pogi" 

QUIT = False

class ClientThread(threading.Thread):
    """
    Thread class to handle communication with a single client.

    Workflow:
    1. Receive client name and number.
    2. If the number is out of range, terminate server.
    3. Otherwise, generate a random number for the server, compute the sum, and send back the response.
    4. Close the client connection when done.
    """
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

            # Display client info
            print(f"Received from client: {client_name.strip()} with number {client_number}")
            print(f"{SERVER_NAME} is handling the connection.")

            # Terminate server if number out of range
            if not (1 <= client_number <= 100):
                print("Client sent number out of range. Shutting down server.")
                QUIT = True
                return

            # Server picks a number and compute sum
            server_number = random.randint(1, 100)
            print(f"Server number: {server_number}, sum: {client_number + server_number}")

            # Send response back to client
            response = f"{SERVER_NAME},{server_number}"
            self.client_socket.sendall(response.encode())
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Close client socket
            self.client_socket.close()

def main():
    """
    Main function to run the server.

    Workflow:
    1. Start a TCP server and listen for client connections.
    2. For each client, spawn a new thread (concurrent handling).
    3. If any client sends an out of range number, set QUIT to True and stop accepting new connections.
    4. Close server on shutdown.
    """
    global QUIT
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"{SERVER_NAME} listening on {HOST}:{PORT}")

    # Accept and Handle clients until QUIT is triggered.
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
    # Shutdown server
    server_socket.close()
    print("Server terminated.")

if __name__ == "__main__":
    main()
