import tkinter as tk
from tkinter import messagebox
import random


COLORS = ["red", "green", "blue", "gold"]
PLAYER_NAMES = ["Red", "Green", "Blue", "Yellow"]
TRACK_LENGTH = 40
FINISH = TRACK_LENGTH - 1

class LudoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Ludo Game")
        self.root.resizable(False, False)

        self.player_count = tk.IntVar(value=4)
        self.players = []
        self.positions = []
        self.current = 0
        self.dice_value = None
        self.game_over = False

        top = tk.Frame(root, padx=10, pady=8)
        top.pack()
        tk.Label(top, text="Number of players:").pack(side="left")
        tk.OptionMenu(top, self.player_count, 2, 3, 4).pack(side="left", padx=5)
        tk.Button(top, text="New Game", command=self.new_game).pack(side="left", padx=5)

        self.status = tk.Label(root, text="", font=("Arial", 12, "bold"), pady=5)
        self.status.pack()

        self.canvas = tk.Canvas(root, width=600, height=400, bg="#f7f4ea")
        self.canvas.pack(padx=10, pady=5)

        controls = tk.Frame(root, pady=8)
        controls.pack()
        self.dice_label = tk.Label(controls, text="Dice: -", font=("Arial", 16, "bold"))
        self.dice_label.pack(side="left", padx=10)
        self.roll_button = tk.Button(controls, text="Roll Dice", font=("Arial", 12),
                                     command=self.roll_dice)
        self.roll_button.pack(side="left", padx=10)
        self.move_button = tk.Button(controls, text="Move Token", font=("Arial", 12),
                                     command=self.move_token, state="disabled")
        self.move_button.pack(side="left", padx=10)

        tk.Label(root, text="Rule: Roll a 6 to start. Reach the final square to win.",
                 font=("Arial", 9), pady=5).pack()

        self.new_game()

    def new_game(self):
        count = self.player_count.get()
        self.players = list(range(count))
        self.positions = [-1] * count  # -1 means token is at home
        self.current = 0
        self.dice_value = None
        self.game_over = False
        self.dice_label.config(text="Dice: -")
        self.move_button.config(state="disabled")
        self.roll_button.config(state="normal")
        self.draw_board()
        self.update_status()

    def track_point(self, position):
        import math
        angle = (2 * math.pi * position / TRACK_LENGTH) - math.pi / 2
        cx, cy = 300, 195
        rx, ry = 205, 130
        return cx + rx * math.cos(angle), cy + ry * math.sin(angle)

    def draw_board(self):
        self.canvas.delete("all")
        self.canvas.create_text(300, 20, text="LUDO", font=("Arial", 18, "bold"), fill="#333333")

        for i in range(TRACK_LENGTH):
            x, y = self.track_point(i)
            r = 12
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="white",
                                    outline="#555555", width=1)
            self.canvas.create_text(x, y, text=str(i+1), font=("Arial", 7), fill="#555555")

        home_spots = [(65, 70), (535, 70), (65, 320), (535, 320)]
        for i in range(self.player_count.get()):
            hx, hy = home_spots[i]
            color = COLORS[i]
            self.canvas.create_rectangle(hx-35, hy-25, hx+35, hy+25,
                                         fill=color, outline="#333333", width=2)
            label = PLAYER_NAMES[i]
            self.canvas.create_text(hx, hy-39, text=label, font=("Arial", 10, "bold"))
            if self.positions[i] == -1:
                self.canvas.create_oval(hx-12, hy-12, hx+12, hy+12,
                                         fill="white", outline=color, width=4)

        for i, pos in enumerate(self.positions):
            if pos >= 0:
                x, y = self.track_point(pos)
                # Small offsets allow tokens to be seen if they share a square.
                x += (i % 2) * 10 - 5
                y += (i // 2) * 10 - 5
                self.canvas.create_oval(x-10, y-10, x+10, y+10,
                                        fill=COLORS[i], outline="black", width=2)
                self.canvas.create_text(x, y, text=str(i+1), fill="white",
                                        font=("Arial", 8, "bold"))

        self.canvas.create_text(300, 380,
                                text="Home tokens start in the coloured boxes",
                                font=("Arial", 9), fill="#555555")

    def update_status(self):
        if not self.game_over:
            self.status.config(text=f"{PLAYER_NAMES[self.current]}'s turn")
        else:
            self.status.config(text="Game over!")

    def roll_dice(self):
        if self.game_over or self.dice_value is not None:
            return
        self.dice_value = random.randint(1, 6)
        self.dice_label.config(text=f"Dice: {self.dice_value}")
        self.roll_button.config(state="disabled")

        if self.positions[self.current] == -1 and self.dice_value != 6:
            self.status.config(text=f"{PLAYER_NAMES[self.current]} rolled {self.dice_value}. Need a 6 to start.")
            self.root.after(900, self.finish_turn)
        elif self.positions[self.current] >= 0 and self.positions[self.current] + self.dice_value > FINISH:
            self.status.config(text="You need the exact number to finish.")
            self.root.after(900, self.finish_turn)
        else:
            self.move_button.config(state="normal")
            self.status.config(text=f"{PLAYER_NAMES[self.current]} rolled {self.dice_value}. Click Move Token.")

    def move_token(self):
        if self.game_over or self.dice_value is None:
            return
        pos = self.positions[self.current]
        if pos == -1:
            self.positions[self.current] = 0
        else:
            self.positions[self.current] += self.dice_value

        if self.positions[self.current] == FINISH:
            self.draw_board()
            self.game_over = True
            self.status.config(text=f"{PLAYER_NAMES[self.current]} wins!")
            self.move_button.config(state="disabled")
            self.roll_button.config(state="disabled")
            messagebox.showinfo("Ludo", f"{PLAYER_NAMES[self.current]} wins!")
            return

        rolled_six = self.dice_value == 6
        self.dice_value = None
        self.dice_label.config(text="Dice: -")
        self.move_button.config(state="disabled")
        self.draw_board()

        if not rolled_six:
            self.current = (self.current + 1) % len(self.players)
        self.roll_button.config(state="normal")
        self.update_status()

    def finish_turn(self):
        if self.game_over:
            return
        self.dice_value = None
        self.dice_label.config(text="Dice: -")
        self.move_button.config(state="disabled")
        self.current = (self.current + 1) % len(self.players)
        self.roll_button.config(state="normal")
        self.update_status()

if __name__ == "__main__":
    root = tk.Tk()
    game = LudoGame(root)
    root.mainloop()
