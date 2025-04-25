import tkinter as tk
import random
import time


GRID_SIZE = 100
PROB_ALIVE = 0.5
MAX_GEN = 250
root = tk.Tk()
gen = tk.IntVar(value=1)
play_pause_btn_text = tk.StringVar(value="Play")
continue_playing = False

def play_pause(grid, canvas, cell_size):
    global continue_playing
    if play_pause_btn_text.get() == "Play":
        play_pause_btn_text.set("Pause")
        continue_playing = True;
        play_to_end(grid, canvas, cell_size)
    else:
        continue_playing = False;
        play_pause_btn_text.set("Play")


def play_to_end(grid, canvas, cell_size):
    global continue_playing
    global gen
    if continue_playing and gen.get() < MAX_GEN:
        next_gen(grid, canvas, cell_size)
        canvas.update()

        canvas.after(50, play_to_end, grid, canvas, cell_size)  # Run again after 50 ms


def next_gen(grid, canvas, cell_size):
    global gen
    if gen.get() % 2 == 1:
        blue_step_no_wrap(grid)
    else:
        red_step_no_wrap(grid)
    draw_grid(canvas, grid, cell_size)
    gen.set(gen.get() + 1)

def back_gen(grid, canvas, cell_size):
    global gen
    if gen.get() > 1:
        gen.set(gen.get() - 1)
        if gen % 2 == 0:
            blue_step_no_wrap(grid)
        else:
            red_step_no_wrap(grid)
        draw_grid(canvas, grid, cell_size)


def change_block_f(grid, i, j):
    b1 = grid[i][j]
    b2 = grid[i + 1][j]
    b3 = grid[i][j + 1]
    b4 = grid[i + 1][j + 1]
    black = b1 + b2 + b3 + b4

    if black != 2:
        b1 = 1 - b1
        b2 = 1 - b2
        b3 = 1 - b3
        b4 = 1 - b4

        if black == 3:
            grid[i][j] = b4
            grid[i + 1][j] = b3
            grid[i][j + 1] = b2
            grid[i + 1][j + 1] = b1
        else:
            grid[i][j] = b1
            grid[i + 1][j] = b2
            grid[i][j + 1] = b3
            grid[i + 1][j + 1] = b4


def red_step_no_wrap(grid):
    #initialize red
    for i in range(1, len(grid) -1, 2):
        for j in range(1, len(grid[0]) - 1, 2):
            change_block_f(grid, i, j)


def blue_step_no_wrap(grid):
     #initialize red
    for i in range(0, len(grid) -1, 2):
        for j in range(0, len(grid[0]) - 1, 2):
            change_block_f(grid, i, j)


def initialize_grid(size, prob_alive=0.5):
    return [
        [1 if random.random() < prob_alive else 0 for _ in range(size)]
        for _ in range(size)
    ]


def draw_grid(canvas, grid, cell_size):
    canvas.delete("all")
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            x0 = j * cell_size
            y0 = i * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            color = "black" if grid[i][j] == 1 else "white"
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="gray")


def initialize_gui(grid):
    root.title("Cellular Automaton")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    adj_height = int(screen_height * 0.9)

    cell_size = min(screen_width // GRID_SIZE, adj_height // GRID_SIZE)

    canvas_width = cell_size * GRID_SIZE
    canvas_height = cell_size * GRID_SIZE

    root.geometry(f"{canvas_width + 200}x{canvas_height}")

    # Creating the toolbar
    toolbar = tk.Frame(root, width=200, bg="lightgray")
    toolbar.pack(side="left", fill="y")

    play_button = tk.Button(toolbar, textvariable=play_pause_btn_text,
                            command=lambda: play_pause(grid, canvas, cell_size))
    play_button.pack(pady=10)

    step_title_label = tk.Label(toolbar, text=f"Step:", font=("Arial", 12))
    step_title_label.pack(pady=10)

    step_no_label = tk.Label(toolbar, textvariable=gen, font=("Arial", 12))
    step_no_label.pack(pady=10)

    next_button = tk.Button(toolbar, text="Next", command=lambda: next_gen(grid, canvas, cell_size))
    next_button.pack(pady=10)

    back_button = tk.Button(toolbar, text="Back", command=lambda: back_gen(grid, canvas, cell_size))
    back_button.pack(pady=10)

    # The canvas for the grid
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack(side="right", fill="both", expand=True)

    draw_grid(canvas, grid, cell_size)

    root.mainloop()


def main():
    grid = initialize_grid(GRID_SIZE, PROB_ALIVE)
    initialize_gui(grid)


if __name__ == "__main__":
    main()