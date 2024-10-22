import socket
import threading

def send_file(s, filename):
    with open(filename, 'rb') as file:
        file_content = file.read()
    
    # Construct a header "FILE" to let server know it's different from normal messages.
    file_info = f"FILE:{filename}:{len(file_content)}:".encode('utf-8')
    
    # Send file_info and file contents together as a single message.
    s.sendall(file_info + file_content)



def receive_message(s):
    while True:
        message = s.recv(1024).decode('utf-8')
        print(f"\nServer: {message}")
        print("Enter message/file (start message w sendfile:): ")

def send_message(s):
    while True:
        message = input("Enter message/file (start message w sendfile:): ")
        if message.startswith("sendfile:"):
            _, filename = message.split()
            send_file(s, filename)
        else:
            s.send(message.encode('utf-8'))

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 9999))
    threading.Thread(target=receive_message, args=(s,)).start()
    threading.Thread(target=send_message, args=(s,)).start()

if __name__ == "__main__":
    main()
