import tkinter as tk
from tkinter import messagebox
import random

class SimpleXOGame:
    def __init__(self, size, win_length, symbol1, symbol2, vs_bot=False, bot_level="easy"):
        self.size = size
        self.win_length = win_length
        self.symbols = [symbol1, symbol2]
        self.current_player = 0
        self.board = [["" for _ in range(size)] for _ in range(size)]
        self.moves = {symbol1: [], symbol2: []}
        self.win_coords = []
        self.vs_bot = vs_bot
        self.bot_level = bot_level
        self.root = tk.Tk()
        self.root.title(f"XO - {self.size}x{self.size}")
        self.root.configure(bg="#2c003e")
        self.status = tk.Label(self.root, text=f"Player {self.symbols[0]}'s turn", font=("Arial", 14),
                               fg="white", bg="#2c003e")
        self.status.grid(row=0, column=0, columnspan=size, pady=5)
        self.buttons = []
        self.build_grid()
        self.restart_btn = tk.Button(self.root, text="Restart", font=("Arial", 12, "bold"),
                                     command=self.restart_game, bg="#6a0dad", fg="white")
        self.restart_btn.grid(row=size+1, column=0, columnspan=size, pady=10)
        self.root.mainloop()

    def build_grid(self):
        for i in range(self.size):
            row = []
            for j in range(self.size):
                btn = tk.Button(self.root, text="", font=("Arial", 24),
                                width=4, height=2, bg="#6a0dad", fg="white",
                                activebackground="#9f5de2",
                                command=lambda i=i, j=j: self.play(i, j))
                btn.grid(row=i+1, column=j, padx=3, pady=3)
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#9f5de2") if b["text"] == "" else None)
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#6a0dad") if b["text"] == "" else None)
                row.append(btn)
            self.buttons.append(row)

    def play(self, i, j):
        symbol = self.symbols[self.current_player]
        if self.board[i][j] == "":
            self.board[i][j] = symbol
            self.buttons[i][j].config(text=symbol, state="disabled")
            self.moves[symbol].append((i, j))

            if len(self.moves[symbol]) > self.win_length:
                old_i, old_j = self.moves[symbol].pop(0)
                self.board[old_i][old_j] = ""
                self.buttons[old_i][old_j].config(text="", state="normal")

            if self.check_win(symbol):
                self.highlight_winner()
                messagebox.showinfo("\U0001F3C6 Winner", f"Player {symbol} wins!")
                self.disable_all()
                self.status.config(text=f"Player {symbol} wins!")
                return

            if all(cell != "" for row in self.board for cell in row):
                messagebox.showinfo("Draw", "It's a draw!")
                self.status.config(text="Draw!")
                return

            self.current_player = 1 - self.current_player
            self.status.config(text=f"Player {self.symbols[self.current_player]}'s turn")

            if self.vs_bot and self.current_player == 1:
                self.root.after(500, self.bot_move)

    def bot_move(self):
        i, j = self.get_bot_move()
        self.play(i, j)

    def get_bot_move(self):
        empty_cells = [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == ""]
        opponent = self.symbols[0]
        bot = self.symbols[1]

        def can_win(symbol):
            for i, j in empty_cells:
                self.board[i][j] = symbol
                self.moves[symbol].append((i, j))
                if self.check_win(symbol):
                    self.board[i][j] = ""
                    self.moves[symbol].pop()
                    return (i, j)
                self.board[i][j] = ""
                self.moves[symbol].pop()
            return None

        if self.bot_level == "hard":
            win = can_win(bot)
            if win:
                return win
            block = can_win(opponent)
            if block:
                return block
            center = (self.size // 2, self.size // 2)
            if self.board[center[0]][center[1]] == "":
                return center
            corners = [(0,0),(0,self.size-1),(self.size-1,0),(self.size-1,self.size-1)]
            random.shuffle(corners)
            for i, j in corners:
                if self.board[i][j] == "":
                    return (i, j)
        return random.choice(empty_cells)

    def check_win(self, symbol):
        coords = set(self.moves[symbol])
        for x, y in coords:
            for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                count = 1
                for dir in [1, -1]:
                    nx, ny = x, y
                    while True:
                        nx += dx * dir
                        ny += dy * dir
                        if (nx, ny) in coords:
                            count += 1
                        else:
                            break
                if count >= self.win_length:
                    self.win_coords = list(coords)
                    return True
        return False

    def highlight_winner(self):
        for i, j in self.win_coords:
            self.buttons[i][j].config(bg="#00cc88")

    def disable_all(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def restart_game(self):
        self.root.destroy()
        show_mode_menu()

def show_mode_menu():
    menu = tk.Tk()
    menu.title("Choose Mode")
    menu.geometry("300x200")
    menu.configure(bg="#2c003e")

    def choose_mode(vs_bot):
        menu.destroy()
        if vs_bot:
            show_bot_level_menu()
        else:
            show_settings(vs_bot)

    tk.Button(menu, text="Play with Friend", font=("Arial", 12), bg="#6a0dad", fg="white",
              command=lambda: choose_mode(False)).pack(pady=20)
    tk.Button(menu, text="Play with Bot", font=("Arial", 12), bg="#6a0dad", fg="white",
              command=lambda: choose_mode(True)).pack(pady=20)
    menu.mainloop()

def show_bot_level_menu():
    menu = tk.Tk()
    menu.title("Choose Bot Level")
    menu.geometry("300x200")
    menu.configure(bg="#2c003e")

    def choose(level):
        menu.destroy()
        show_settings(True, level)

    tk.Button(menu, text="Easy", font=("Arial", 12), bg="#6a0dad", fg="white",
              command=lambda: choose("easy")).pack(pady=20)
    tk.Button(menu, text="Medium", font=("Arial", 12), bg="#6a0dad", fg="white",
              command=lambda: choose("medium")).pack(pady=10)
    tk.Button(menu, text="Hard", font=("Arial", 12), bg="#6a0dad", fg="white",
              command=lambda: choose("hard")).pack(pady=10)
    menu.mainloop()

def show_settings(vs_bot=False, bot_level="easy"):
    menu = tk.Tk()
    menu.title("Choose Settings")
    menu.geometry("420x700")
    menu.configure(bg="#2c003e")

    canvas = tk.Canvas(menu, bg="#2c003e", highlightthickness=0)
    frame = tk.Frame(canvas, bg="#2c003e")
    scrollbar = tk.Scrollbar(menu, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    frame.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    tk.Label(frame, text="Choose player symbols", font=("Arial", 14, "bold"),
             bg="#2c003e", fg="white").pack(pady=10)

    symbols = ["X", "O", "⭐", "🔥", "🐱", "🍕", "💀", "🌟"]
    symbol1_var = tk.StringVar(value="X")
    symbol2_var = tk.StringVar(value="O")

    row_frame = tk.Frame(frame, bg="#2c003e")
    row_frame.pack()

    tk.Label(row_frame, text="Player 1", font=("Arial", 12), fg="white", bg="#2c003e").grid(row=0, column=0, padx=20)
    tk.Label(row_frame, text="Player 2", font=("Arial", 12), fg="white", bg="#2c003e").grid(row=0, column=1, padx=20)

    for i, sym in enumerate(symbols):
        tk.Radiobutton(row_frame, text=sym, variable=symbol1_var, value=sym,
                       bg="#2c003e", fg="white", selectcolor="#6a0dad").grid(row=i+1, column=0)
        tk.Radiobutton(row_frame, text=sym, variable=symbol2_var, value=sym,
                       bg="#2c003e", fg="white", selectcolor="#6a0dad").grid(row=i+1, column=1)

    tk.Label(frame, text="Board size:", font=("Arial", 14), fg="white", bg="#2c003e").pack(pady=15)
    size_var = tk.IntVar(value=3)
    for size in range(3, 6):
        tk.Radiobutton(frame, text=f"{size} x {size}", variable=size_var, value=size,
                       bg="#2c003e", fg="white", selectcolor="#6a0dad",
                       font=("Arial", 12)).pack()

    win_slider_label = tk.Label(frame, text="", fg="white", bg="#2c003e", font=("Arial", 12))
    win_slider = tk.Scale(frame, from_=3, to=3, orient="horizontal", bg="#2c003e", fg="white",
                          highlightthickness=0, troughcolor="#6a0dad", length=200)

    def update_slider(*args):
        board_size = size_var.get()
        win_slider.config(to=board_size)
        if win_slider.get() > board_size:
            win_slider.set(board_size)
        win_slider_label.config(text=f"Win condition: {win_slider.get()} in a row")

    def slider_update_text(val):
        win_slider_label.config(text=f"Win condition: {val} in a row")

    size_var.trace_add("write", update_slider)
    win_slider.config(command=slider_update_text)
    update_slider()
    win_slider_label.pack(pady=(15, 5))
    win_slider.pack()

    def start():
        s1 = symbol1_var.get()
        s2 = symbol2_var.get()
        if s1 == s2:
            messagebox.showerror("Error", "Symbols must be different!")
            return
        board_size = size_var.get()
        win_len = win_slider.get()
        menu.destroy()
        SimpleXOGame(board_size, win_len, s1, s2, vs_bot, bot_level)

    tk.Button(frame, text="Start Game", font=("Arial", 12, "bold"),
              bg="#6a0dad", fg="white", command=start).pack(pady=20)

    menu.mainloop()

if __name__ == "__main__":
    show_mode_menu()