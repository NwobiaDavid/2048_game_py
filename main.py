import tkinter as tk
import random

class Game2048:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("2048 Game")

        self.grid_size = 4
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]

        self.score = 0

        self.create_gui()
        self.init_game()

    def create_gui(self):
        self.main_frame = tk.Frame(self.root, bg="lightgray")
        self.main_frame.pack(padx=10, pady=10)

        self.score_label = tk.Label(self.root, text="Score: 0", font=("Helvetica", 16))
        self.score_label.pack(pady=10)

        self.cells = [[tk.Label(self.main_frame, text="", font=("Helvetica", 24), width=5, height=2, bd=2, relief="ridge")
                       for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.cells[i][j].grid(row=i, column=j, padx=5, pady=5)

        restart_button_style = {'font': ('Helvetica', 12),
                                'background': '#000',
                                'foreground': 'white',
                                'borderwidth': 2,
                                'relief': 'raised',
                                'pady': 5,
                                'command': self.reset_game}

        self.restart_button = tk.Button(self.root, text="Restart", **restart_button_style)
        self.restart_button.pack(pady=10)

        self.root.bind("<Left>", lambda event: self.move("left"))
        self.root.bind("<Right>", lambda event: self.move("right"))
        self.root.bind("<Up>", lambda event: self.move("up"))
        self.root.bind("<Down>", lambda event: self.move("down"))

    def init_game(self):
        self.add_random_tile()
        self.add_random_tile()
        self.update_gui()
        self.reset_game()

    def reset_game(self):
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()
        self.update_gui()


    def add_random_tile(self):
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def update_gui(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.grid[i][j]
                text = str(value) if value > 0 else ""
                color = "white" if value < 8 else "black"
                self.cells[i][j].config(text=text, bg=self.get_tile_color(value), fg=color)

        self.score_label.config(text=f"Score: {self.score}")

    def get_tile_color(self, value):
        colors = {
            2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
            32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
            512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }
        return colors.get(value, "#cdc1b4")

    def move(self, direction):
        before_move = [row[:] for row in self.grid]

        if direction == "left":
            self.move_left()
        elif direction == "right":
            self.move_right()
        elif direction == "up":
            self.move_up()
        elif direction == "down":
            self.move_down()

        after_move = [row[:] for row in self.grid]

        if before_move != after_move:
            self.add_random_tile()
            self.update_gui()

    def move_left(self):
        for i in range(self.grid_size):
            self.grid[i] = self.slide_and_merge(self.grid[i])

    def move_right(self):
        for i in range(self.grid_size):
            row = self.grid[i][::-1]
            row = self.slide_and_merge(row)
            self.grid[i] = row[::-1]

    def move_up(self):
        for j in range(self.grid_size):
            col = [self.grid[i][j] for i in range(self.grid_size)]
            col = self.slide_and_merge(col)
            for i in range(self.grid_size):
                self.grid[i][j] = col[i]

    def move_down(self):
        for j in range(self.grid_size):
            col = [self.grid[i][j] for i in range(self.grid_size)][::-1]
            col = self.slide_and_merge(col)
            for i in range(self.grid_size):
                self.grid[i][j] = col[self.grid_size - 1 - i]

    def slide_and_merge(self, line):
        new_line = [0] * self.grid_size
        merged = [False] * self.grid_size
        index = 0

        for i in range(self.grid_size):
            if line[i] != 0:
                if index > 0 and new_line[index - 1] == line[i] and not merged[index - 1]:
                    new_line[index - 1] *= 2
                    merged[index - 1] = True
                    self.score += new_line[index - 1]
                else:
                    new_line[index] = line[i]
                    index += 1
        return new_line


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = Game2048()
    game.run()
