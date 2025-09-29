import socket

HOST = "127.0.0.1"  # server IP
PORT = 5050         # server port
CLIENT_NAME = "Client of Your Name"  # replace with your name

def main():
    try:
        # Get integer input
        client_number = int(input("Enter an integer (1-100): "))
        if not (1 <= client_number <= 100):
            print("Number out of range! Exiting.")
            return

        # Connect to server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")

        # Send client name and number
        message = f"{CLIENT_NAME},{client_number}"
        sock.sendall(message.encode())

        # Receive server response
        data = sock.recv(1024).decode()
        server_name, server_number_str = data.split(',')
        server_number = int(server_number_str)

        # Display results
        print(f"Client: {CLIENT_NAME}, Number: {client_number}")
        print(f"Server: {server_name.strip()}, Number: {server_number}")
        print(f"Sum: {client_number + server_number}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()
        print("Client terminated.")

if __name__ == "__main__":
    main()
