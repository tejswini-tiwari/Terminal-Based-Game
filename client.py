import socket
import curses
import threading

HOST = '127.0.0.1'  
PORT = 65433       
latest_game_state = ""
running = True

def receive_data(s):
    global latest_game_state
    global running
    try:
        while running:
            data = s.recv(1024)
            if not data:
                break
            latest_game_state = data.decode('utf-8')
    except (ConnectionResetError, BrokenPipeError):
        print("Connection to server lost.")
    finally:
        running = False

def main(stdscr):
    global running
    stdscr.nodelay(True) 
    stdscr.clear()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            
            receive_thread = threading.Thread(target=receive_data, args=(s,), daemon=True)
            receive_thread.start()
            
            while running:
                stdscr.clear()
                height, width = stdscr.getmaxyx()
                
                display_text = latest_game_state
                stdscr.addstr(height // 2, width // 2 - len(display_text) // 2, display_text)
                
                key = stdscr.getch()
                if key == ord('q'):
                    running = False
                
                stdscr.refresh()
                curses.napms(100) 
                
        except ConnectionRefusedError:
            stdscr.addstr(0, 0, "Could not connect to the server. Is it running?")
            stdscr.refresh()
            curses.napms(3000) 

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except Exception as e:
        print(f"An error occurred: {e}")