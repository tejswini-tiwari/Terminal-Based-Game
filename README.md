Tic-Tac-Toe (Network Multiplayer)

This is a simple two-player Tic-Tac-Toe game that works over a network.
One program acts as the server (the game host), and two people can connect as clients to play against each other.

It uses:

Python sockets (TCP) → for reliable communication between players.

Curses library → for a nice terminal-based game board on the client side.

JSON messages → so server and clients can talk in a structured way.

How it Works

The server waits for two players to connect.

Each player is assigned a symbol: X or O.

Players take turns making moves.

The server checks if someone has won or if the game is a draw.

The board updates on both clients after every move.

Requirements

Python 3.x

Works on Linux, Mac, and Windows (Windows needs a terminal that supports curses, like Git Bash or WSL).

Setup

Clone or download the files. You should have:

server.py → runs the server

client.py → runs the player interface

Running the Game

Start the server (in one terminal):

python3 server.py


By default, it runs on port 65432.
You can also pick a port:

python3 server.py 5000


Start two clients (in separate terminals):

python3 client.py


The first client will be assigned X

The second client will be assigned O

Play!

Controls

Arrow keys / WASD → Move selection around the board

Enter / Return → Place your mark

Numbers 1–9 → Quick move (corresponds to board positions)

q → Quit game

n → Start a new game (after one finishes)

Game Rules

X always starts first

You win by placing 3 of your marks in a row (horizontally, vertically, or diagonally)

If the board fills with no winner → it’s a draw
