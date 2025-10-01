import socket
import random

# server configuration
HOST = "127.0.0.1"  # server IP
PORT = 5050         # server port

CLIENT_NAMES = ["David Javier", "Zach Hallare"]  # client names chooses one randomly each run  
CLIENT_NAME = random.choice(CLIENT_NAMES) 

def main():
    """
    Main function/s of client program.
    
    Workflow:
    1. Ask the user for an integer (1-100)
    2. Connect to the server via TCP
    3. Send client name and chose number to the server.
    4. Wait for the server's response.
        - If valid, display the client info, server, info, and their sum.
        - If invalid, client will also terminate.
    5. Close the connection before exiting.
    """ 

    sock = None
    try:
        # Get integer input
        client_number = int(input("Enter an integer (1-100): "))

        # Connect to server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")

        # Send client name and number
        message = f"{CLIENT_NAME},{client_number}"
        sock.sendall(message.encode())

        # Receive and validate server response
        data = sock.recv(1024).decode()
        if not data or ',' not in data:
            print("Server sent invalid response.")
            return      
        server_name, server_number_str = data.split(',')
        server_number = int(server_number_str)

        # Display results from server
        print(f"Client: {CLIENT_NAME}, Number: {client_number}")
        print(f"Server: {server_name.strip()}, Number: {server_number}")
        print(f"Sum: {client_number + server_number}")


    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close socket connection
        if sock:
            sock.close()
            print("Client terminated.")

if __name__ == "__main__":
    main()
