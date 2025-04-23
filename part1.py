import tkinter as tk
import random


GRID_SIZE = 100


PROB_ALIVE = 0.5

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

    cell_size = min(screen_width // GRID_SIZE, screen_height // GRID_SIZE)

    canvas_width = cell_size * GRID_SIZE
    canvas_height = cell_size * GRID_SIZE
    
    root.geometry(f"{canvas_width}x{canvas_height}")

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
    canvas.pack()

    grid = initialize_grid(GRID_SIZE, PROB_ALIVE)
    draw_grid(canvas, grid, cell_size)

    root.mainloop()

if __name__ == "__main__":
    main()