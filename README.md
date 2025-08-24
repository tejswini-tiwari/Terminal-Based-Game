# 🎮 Terminal Tic-Tac-Toe (Multiplayer)

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Contributors](https://img.shields.io/badge/Contributors-2-orange)](https://github.com/<your-username>/terminal-tic-tac-toe/graphs/contributors)

A **real-time, terminal-based multiplayer Tic-Tac-Toe game** built with Python sockets and JSON messaging. Play locally on the same machine or over a network with your friends!

![Gameplay Demo](assets/demo.gif)


---

## 🚀 Features

* Real-time multiplayer gameplay with two players
* Automatic player mark assignment (`X` / `O`)
* Input validation (1-9 positions, occupied cells handled)
* Win/draw detection
* Handles player disconnects gracefully
* ASCII-based board display for terminal fun

---

## 💻 Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/terminal-tic-tac-toe.git
cd terminal-tic-tac-toe
```

### Run Locally (Same Computer)

1. Open **two terminal windows**.
2. Start the server:

```bash
python server.py 65432
```

3. Start **two clients** (in separate terminals):

```bash
python client.py 127.0.0.1 65432
```

### Run Over Network

1. Start the server on a host machine:

```bash
python server.py 65432
```

2. Other players connect from their machines:

```bash
python client.py <SERVER_IP> 65432
```

---

## 🎮 How to Play

* Board positions are numbered **1–9**:

```
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
```

* Enter a number (1-9) to place your mark.
* Enter `q` or `quit` to exit the game.
* The server automatically checks for **wins or draw** and announces the result.

---

## 🛠️ Contributing

We welcome contributions! Follow these steps to raise a pull request:

1. **Fork** the repository.
2. **Clone** your fork:

```bash
git clone https://github.com/<your-username>/terminal-tic-tac-toe.git
```

3. **Create a branch**:

```bash
git checkout -b feature/new-feature
```

4. Make your changes and **commit**:

```bash
git add .
git commit -m "Add feature: <feature description>"
```

5. **Push** your branch:

```bash
git push origin feature/new-feature
```

6. Open a **pull request** on the original repository.

---

## 📈 Roadmap (Future Enhancements)

* Add **AI opponent** for single-player mode
* Support **more than two players** with larger boards
* Add **score tracking** and game history
* Add **color-coded terminal board** for better visuals

---

## 🙏 Acknowledgements

* Inspired by classic Tic-Tac-Toe games.
* Thanks to the Python community for socket programming examples.



