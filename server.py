import socket
import threading
import time

HOST = '127.0.0.1'  
PORT = 65433   

clients = []
game_state = "Hello from the server! Waiting for a second player..."

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    global game_state
    
    clients.append(conn)
    
    try:
        while True:
            time.sleep(1)
            conn.sendall(game_state.encode('utf-8'))
    
    except (ConnectionResetError, BrokenPipeError):
        print(f"Client {addr} disconnected.")
        clients.remove(conn)

def broadcast_game_state():
    global game_state
    
    while True:
        game_state = f"The current time  {time.ctime()} and there are {len(clients)} players connected."
        time.sleep(1)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        
        threading.Thread(target=broadcast_game_state, daemon=True).start()
        
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == '__main__':
    start_server()