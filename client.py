
import socket, json, sys

def send_json(sock, obj):
    sock.sendall((json.dumps(obj) + '\n').encode())

def recv_json(sock_file):
    line = sock_file.readline()
    if not line:
        return None
    return json.loads(line.strip())

def print_board(board):
    print()
    print(f" {board[0]} | {board[1]} | {board[2]}    1 | 2 | 3")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]}    4 | 5 | 6")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]}    7 | 8 | 9")
    print()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 client.py SERVER_IP [PORT]")
        sys.exit(1)

    HOST = sys.argv[1]
    PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 65432

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock_file = sock.makefile('r', encoding='utf-8')

    my_mark = None
    print(f"Connected to {HOST}:{PORT}. Waiting for assignment...")

    try:
        while True:
            msg = recv_json(sock_file)
            if msg is None:
                print("Server closed the connection.")
                break

            t = msg.get('type')
            if t == 'assign':
                my_mark = msg.get('mark')
                print("You are:", my_mark)
            elif t == 'message':
                print("[server]", msg.get('text'))
            elif t == 'state':
                board = msg.get('board')
                status = msg.get('status')
                turn = msg.get('turn')
                result = msg.get('result')
                print_board(board)

                if status == 'ongoing':
                    if turn == my_mark:
                        # get move from user and send it
                        while True:
                            s = input(f"Your move ({my_mark}). Enter position 1-9 (or 'q' to quit): ").strip()
                            if s.lower() in ('q','quit','exit'):
                                print("Quitting.")
                                sock.close()
                                return
                            try:
                                pos = int(s)
                                if not (1 <= pos <= 9):
                                    print("Choose number 1-9.")
                                    continue
                                send_json(sock, {'type': 'move', 'pos': pos})
                                break
                            except ValueError:
                                print("Enter a number 1-9.")
                    else:
                        print(f"Waiting for opponent (mark {turn}) to move...")
                elif status == 'finished':
                    if result == 'draw':
                        print("Game finished: Draw.")
                    else:
                        if result == my_mark:
                            print("Game finished: YOU WIN! 🎉")
                        else:
                            print("Game finished: YOU LOSE.")
                    print("Connection will close.")
                    break
            elif t == 'invalid':
                print("Invalid move:", msg.get('reason'))
            else:
                print("Received unknown message:", msg)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        try: sock_file.close()
        except: pass
        try: sock.close()
        except: pass

if __name__ == '__main__':
    main()
