
import socket, json, sys

def send_json(sock, obj):
    try:
        sock.sendall((json.dumps(obj) + '\n').encode())
    except Exception:
        pass

def recv_json(file):
    try:
        line = file.readline()  # blocking until newline
        if not line:
            return None
        return json.loads(line.strip())
    except Exception:
        return None

def check_win(board, player):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    return any(board[a]==board[b]==board[c]==player for a,b,c in wins)

def board_full(board):
    return all(cell != ' ' for cell in board)

def main():
    HOST = '0.0.0.0'
    PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 65432

    print(f"Server starting on {HOST}:{PORT} ... (waiting for 2 players)")
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind((HOST, PORT))
    listen_sock.listen(2)

    clients = []
    try:
        while len(clients) < 2:
            conn, addr = listen_sock.accept()
            print("Connected:", addr)
            file = conn.makefile('r', encoding='utf-8')
            clients.append({'sock': conn, 'file': file, 'addr': addr})
            # Inform connected client how many left to wait for
            send_json(conn, {'type': 'message', 'text': f'Connected to server. Waiting for {2-len(clients)} more player(s)...'})

        # assign marks
        clients[0]['mark'] = 'X'
        clients[1]['mark'] = 'O'
        players = {c['mark']: c for c in clients}

        send_json(players['X']['sock'], {'type': 'assign', 'mark': 'X'})
        send_json(players['O']['sock'], {'type': 'assign', 'mark': 'O'})

        board = [' '] * 9
        current = 'X'  # X starts

        while True:
            # broadcast current state
            for c in clients:
                send_json(c['sock'], {'type': 'state', 'board': board, 'turn': current, 'status': 'ongoing'})

            cur = players[current]
            send_json(cur['sock'], {'type': 'message', 'text': "Your turn. Send {'type':'move','pos':<1-9>}."})

            msg = recv_json(cur['file'])
            if msg is None:
                # current disconnected -> award win to other
                other_mark = 'O' if current == 'X' else 'X'
                other = players.get(other_mark)
                if other:
                    send_json(other['sock'], {'type': 'message', 'text': 'Opponent disconnected. You win by default.'})
                    send_json(other['sock'], {'type': 'state', 'board': board, 'turn': None, 'status': 'finished', 'result': other_mark})
                print("Player disconnected; ending game.")
                break

            if msg.get('type') != 'move' or 'pos' not in msg:
                send_json(cur['sock'], {'type': 'invalid', 'reason': "Expected {'type':'move','pos':<1-9>}."})
                continue

            try:
                pos = int(msg['pos'])
            except Exception:
                send_json(cur['sock'], {'type': 'invalid', 'reason': 'pos must be an integer 1-9.'})
                continue

            if not (1 <= pos <= 9):
                send_json(cur['sock'], {'type': 'invalid', 'reason': 'pos out of range (1-9).'})
                continue

            idx = pos - 1
            if board[idx] != ' ':
                send_json(cur['sock'], {'type': 'invalid', 'reason': 'Cell already taken.'})
                continue

            # make move
            board[idx] = current

            # check win
            if check_win(board, current):
                for c in clients:
                    send_json(c['sock'], {'type': 'state', 'board': board, 'turn': None, 'status': 'finished', 'result': current})
                print(f"Player {current} wins.")
                break

            # check draw
            
            if board_full(board):
                for c in clients:
                    send_json(c['sock'], {'type': 'state', 'board': board, 'turn': None, 'status': 'finished', 'result': 'draw'})
                print("Game draw.")
                break

            # swap turn
            current = 'O' if current == 'X' else 'X'

    finally:
        for c in clients:
            try: c['file'].close()
            except: pass
            try: c['sock'].close()
            except: pass
        listen_sock.close()

if _name_ == '_main_':
    main()
