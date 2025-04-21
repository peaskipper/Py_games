# 🧠 Tic-Tac-Toe with a Twist (Python + Tkinter)

A minimal 2-player Tic-Tac-Toe game made in Python using Tkinter — but with a brainy twist to make it more competitive!

---

## 🔄 The Twist

Unlike classic Tic-Tac-Toe, **each player may only have 3 active marks on the board at a time**. On their 4th turn:
- Their **oldest mark fades**, locking the tile **just for that turn**.
- They must place the new mark on a different tile.
- On the following turn, the faded tile becomes available again.

🎯 This eliminates stalemates, ensures perpetual play, and rewards extensive strategy!

---

## ✨ Features

- 🎮 **2-Player local game** with alternating turns.
- 🌀 **Fading logic**: Only 3 active marks per player; oldest fades on the 4th turn.
- 🔐 **One-turn tile lock** to prevent instant re-claiming of faded spot.
- 🧠 **Win condition detection** for all rows, columns, and diagonals.
- 🎉 **Game end status** with win/draw detection.
- 🔁 **Restart button** to play again instantly.
- 🧼 Clean, minimalist GUI using built-in **Tkinter**.

---

## 🧰 Requirements

Just Python — no external packages!

### ✅ Python 3.x

If you're using a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
