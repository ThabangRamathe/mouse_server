import socket
import pyautogui

def leftClick():
    pyautogui.mouseDown(button='left')
    pyautogui.mouseUp(button='left')

def rightClick():
    pyautogui.mouseDown(button='right')
    pyautogui.mouseUp(button='right')

def moveCursor(data):
    x, y = data.strip().split(",")
    pyautogui.moveTo(float(x), float(y), duration= 0)

def getCursorCoords():
    x, y = pyautogui.position()
    return str(x) + "," + str(y)

def getHostname():
    return socket.gethostname()

def handle_client(client_socket):
    print(f"Client connected: {client_socket.getpeername()}")

    connected = True

    while connected:
        try:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break

            print(f"Received command from client: {data}")

            for command in data.split("!"):
                if command[:1] == 'M':
                    moveCursor(command[2:])
                elif command == 'L':
                    leftClick()
                elif command == 'R':
                    rightClick()
                elif command == 'pos':
                    coords = getCursorCoords()
                    client_socket.sendall(coords.encode())
                elif command == 'name':
                    client_socket.sendall(getHostname().encode())
                    connected = False
                    break
        except Exception as e:
            print(f"Error handling client: {str(e)}")
            break

    print(f"Client disconnected: {client_socket.getpeername()}")
    client_socket.close()

def main():
    server_host = socket.gethostbyname(socket.gethostname())
    server_port = 1999

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(5)  # Maximum 5 connections in the queue

    print(f"Server listening on {server_host}:{server_port}")

    try:
        while True:
            client_socket, address = server_socket.accept()
            handle_client(client_socket)
    except KeyboardInterrupt:
        print("Server shutting down.")
        server_socket.close()

if __name__ == "__main__":
    main()
