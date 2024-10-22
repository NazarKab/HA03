import socket
import threading

def send_message(client_socket):
    while True:
        message = input("\nEnter message to client: ")
        client_socket.send(message.encode('utf-8'))

def handle_client(client_socket):
    threading.Thread(target=send_message, args=(client_socket,)).start()
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if message.startswith("FILE:"):
            _, filename, file_content_start = message.split(":", 2)
            
            file_content = file_content_start.encode('utf-8')
            
            print(f"\nReceived file: {filename}")

            try:
                print("File content:\n", file_content.decode('utf-8'))
            except UnicodeDecodeError:
                print("Unable to display content")

            print("Enter message to client: ")
        else:
            print(f"\nClient: {message}")
            print("Enter message to client: ")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(1)
    print("Server listening on port 9999")

    while True:
        client_socket, address = server.accept()
        print(f"Accepted connection from {address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
