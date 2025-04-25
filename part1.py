import tkinter as tk
import random
import time


GRID_SIZE = 100
PROB_ALIVE = 0.5
gen = 1

def play_to_end(grid, canvas, cell_size):
    global gen
    for i in range(gen, 251):
        next_gen(grid, canvas, cell_size)
        canvas.update()
        time.sleep(0.05)


def next_gen(grid, canvas, cell_size):
    global gen
    if (gen % 2 == 1):
        blue_step_no_wrap(grid)

    else:
        red_step_no_wrap(grid)
    gen += 1
    draw_grid(canvas, grid, cell_size)

def back_gen(grid, canvas, cell_size):
    global gen
    gen -= 1
    if (gen % 2 == 0):
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
    if(black == 3):
        b1 = 1 - b1
        b2 = 1 - b2
        b3 = 1- b3
        b4 = 1 - b4
        grid[i][j] = b4
        grid[i + 1][j] = b3
        grid[i][j + 1] = b2
        grid[i + 1][j + 1] = b1
    if(black not in (2, 3)):
        b1 = 1 - b1
        b2 = 1 - b2
        b3 = 1- b3
        b4 = 1 - b4
        grid[i][j] = b1
        grid[i + 1][j] = b2
        grid[i][j + 1] = b3
        grid[i + 1][j + 1] = b4





def red_step_no_wrap(grid):
    ##initialize red
    for i in range(1, len(grid) -1, 2):
        for j in range(1, len(grid[0]) - 1, 2):
            change_block_f(grid, i, j)
           




def blue_step_no_wrap(grid):
     ##initialize red
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


def main():
    grid = initialize_grid(GRID_SIZE, PROB_ALIVE)

    root = tk.Tk()
    root.title("Cellular Automaton")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    adj_height = int(screen_height * 0.9)

    cell_size = min(screen_width // GRID_SIZE, adj_height // GRID_SIZE)

    canvas_width = cell_size * GRID_SIZE
    canvas_height = cell_size * GRID_SIZE
    
    root.geometry(f"{canvas_width + 200}x{canvas_height}")

    ## Creating the toolbar
    toolbar = tk.Frame(root, width=200, bg="lightgray")
    toolbar.pack(side="left", fill="y")

    play_button = tk.Button(toolbar, text="Play", command=lambda: play_to_end(grid, canvas, cell_size))
    play_button.pack(pady=10)

    step_label = tk.Label(toolbar, text=f"Step:", font=("Arial", 12))
    step_label.pack(pady=10)

    next_button = tk.Button(toolbar, text="Next", command=lambda: next_gen(grid, canvas, cell_size))
    next_button.pack(pady=10)

    back_button = tk.Button(toolbar, text="Back", command=lambda: back_gen(grid, canvas, cell_size))
    back_button.pack(pady=10)



    ## The canvas for the grid
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack(side="right", fill="both", expand=True)

    draw_grid(canvas, grid, cell_size)

    root.mainloop()

if __name__ == "__main__":
    main()