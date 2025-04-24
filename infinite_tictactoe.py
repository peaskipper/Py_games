import tkinter as tk
from tkinter import messagebox
import logging
from collections import deque
import random

# -----------------------------
# Logging setup for debugging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -----------------------------
# Game Configuration Constants
# -----------------------------
BOARD_SIZE = 7  # 3x3 board
ACTIVE_MARK_LIMIT = 7  # Only 3 active marks allowed per player

PLAYERS = ["x", "o"]
EMPTY = ""

# Colors for GUI styling
MARK_COLORS = {
    PLAYERS[0]: "#ffc7e3",
    PLAYERS[1]: "#c7ffca",
    "FADED": "#525252"
}

BG_COLOR = "#0d0d0d"
FONT = ("Century Gothic", 20)
LABEL_FG_COLOR = "#f1faee"

BUTTON_SIZE = 6  # Characters wide
BUTTON_COLOR = "#333333"
BUTTON_FG_COLOR = "#f1faee"


# -----------------------------
# GUI class and game logic
# -----------------------------
class TicTacToeGame:
    """
    2-Player Tic Tac Toe with a twist:
    - Only 3 active marks (x or o) per player can remain on the board.
    - Oldest mark fades when a new one is placed.
    - Faded mark cannot be reclaimed by the immediate next move.
    """
    def __init__(self):

        # Tkinter window setup
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe - Competetive Twist")
        self.root.configure(bg=BG_COLOR)

        # Create empty board
        self._new_game()

        # Add reset button    
        self.restart_button = tk.Button(
            self.root, 
            text="Restart Game", 
            bg=BUTTON_COLOR,              
            fg=BUTTON_FG_COLOR,
            relief="flat",
            borderwidth=0,
            command=self._new_game
            )
        self.restart_button.grid(row=BOARD_SIZE + 2, column=0, columnspan=BOARD_SIZE, pady=10)

        # Start the game loop
        self.root.mainloop()

    def _starting_player(self):
        self.x = PLAYERS[0]
        self.o = PLAYERS[1]
        return random.choice(PLAYERS)

    def _new_game(self):

        # Game state setup
        self.board = [["" for i in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
        self.buttons = [[None for i in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
        self.current_player = self._starting_player()
        self.moves_x = []
        self.moves_o = []
        self.faded_x = []
        self.faded_o = []
        self.move_counter_x = 0
        self.move_counter_o = 0

        # Turn label 
        self.status_label = tk.Label(
            self.root,
            text=f"Turn: {self.current_player}",
            font=FONT,
            fg=LABEL_FG_COLOR,
            bg=BG_COLOR
        )
        self.status_label.grid(row=0, column=0, columnspan=BOARD_SIZE, pady=(10, 10), sticky="nsew")

        # Create board buttons
        self.status_label.config(text=f"Turn: {self.current_player}")
        self._create_board()

    def _create_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                btn = tk.Button(
                    self.root,
                    text="",
                    width=BUTTON_SIZE,
                    height=2,
                    font=FONT,
                    bg=BUTTON_COLOR,              
                    fg=BUTTON_FG_COLOR,             # I don't know wht this does, but removing this breaks stuff
                    relief="flat",
                    borderwidth=0,                  
                    command=lambda r=row, c=col: self._handle_click(r, c)
                )
                btn.grid(row=row + 1, column=col, padx=7, pady=7, sticky="nsew")  # +1 for status label row
                self.buttons[row][col] = btn
                

        for i in range(BOARD_SIZE + 1):  # +1 for status label row
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

    def _handle_click(self, row, col):
        # Reject invalid moves
        if self.board[row][col] != "" or (self.current_player == self.x and (row, col) in self.faded_x) or (self.current_player == self.o and (row, col) in self.faded_o):
            return  
        
        # Reset old tiles
        self._reset_tile()

        # Place the current player's mark
        self.board[row][col] = self.current_player
        self._update_moves(row, col)
        
        # Update the button's visual (for the clicked cell)
        self.buttons[row][col].config(text=self.current_player, fg=MARK_COLORS[self.current_player])

        # Check for win condition
        if len(self.moves_x) == ACTIVE_MARK_LIMIT or len(self.moves_o) == ACTIVE_MARK_LIMIT:
            if self._check_win(self.current_player):
                self._end_game(f"{self.current_player} wins!")
                return
        
        # Switch player turn
        self.current_player = self.o if self.current_player == self.x else self.x
        self._update_status_label()

        # Fade the oldest mark if this is the 4th move for the player
        if (self.current_player == self.x and len(self.moves_x) == ACTIVE_MARK_LIMIT) or (self.current_player == self.o and len(self.moves_o) == ACTIVE_MARK_LIMIT):
            self._fade_oldest_mark()
                
    def _update_moves(self, row, col):
        if self.current_player == self.x:
            self.moves_x.append((row, col))
            self.move_counter_x += 1
        else:
            self.moves_o.append((row, col))
            self.move_counter_o += 1

    def _update_status_label(self):
        self.status_label.config(text=f"Turn: {self.current_player}")

    def _reset_tile(self):
        if self.current_player == self.x and self.faded_x:
            oldest_move = self.faded_x.pop()
            self.board[oldest_move[0]][oldest_move[1]] = ""
            self.buttons[oldest_move[0]][oldest_move[1]].config(text="")

        elif self.current_player == self.o and self.faded_o:
            oldest_move = self.faded_o.pop()
            self.board[oldest_move[0]][oldest_move[1]] = ""
            self.buttons[oldest_move[0]][oldest_move[1]].config(text="")    

    def _fade_oldest_mark(self):
        if self.current_player == self.x and self.moves_x:
            # Get and remove the oldest move for x
            oldest_move = self.moves_x.pop(0)
            self.faded_x = [oldest_move]
            # self.faded_x.append(oldest_move)
            self.board[oldest_move[0]][oldest_move[1]] = "FADED"
            self.buttons[oldest_move[0]][oldest_move[1]].config(fg=MARK_COLORS["FADED"])

        elif self.current_player == self.o and self.moves_o:
            # Get and remove the oldest move for o
            oldest_move = self.moves_o.pop(0)
            self.faded_o = [oldest_move]
            # self.faded_o.append(oldest_move)
            self.board[oldest_move[0]][oldest_move[1]] = "FADED"
            self.buttons[oldest_move[0]][oldest_move[1]].config(fg=MARK_COLORS["FADED"])

    def _check_win(self, player):
        # Check rows
        for row in range(BOARD_SIZE):
            if all(self.board[row][col] == player for col in range(BOARD_SIZE)):
                return True

        # Check columns
        for col in range(BOARD_SIZE):
            if all(self.board[row][col] == player for row in range(BOARD_SIZE)):
                return True

        # Check diagonals
        if all(self.board[i][i] == player for i in range(BOARD_SIZE)):
            return True
        if all(self.board[i][BOARD_SIZE - i - 1] == player for i in range(BOARD_SIZE)):
            return True

        return False

    def _end_game(self, result_text):
        # Show result and disable the board
        self.status_label.config(text=result_text)
        move_counter = self.move_counter_x if self.move_counter_x > self.move_counter_o else self.move_counter_o
        print(f'{result_text} In {move_counter} moves!')
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")


# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":
    logging.info("Starting Tic Tac Toe game with twist...")
    TicTacToeGame()
