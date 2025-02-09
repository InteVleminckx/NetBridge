import socket

class Client:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        """Connect to the server."""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")

    def close(self):
        """Close the connection."""
        if self.client_socket:
            self.client_socket.close()
            print("Connection closed.")
        else:
            raise Exception("Client is not connected to the server.")
