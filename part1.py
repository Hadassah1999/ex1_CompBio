import tkinter as tk
import random


GRID_SIZE = 100
CELL_SIZE= 10

PROB_ALIVE = 0.5

def initialize_grid(size, prob_alive=0.5):
    return [
        [1 if random.random() < prob_alive else 0 for _ in range(size)]
        for _ in range(size)
    ]


    
def draw_grid(canvas, grid):
    canvas.delete("all")
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            x0 = j * CELL_SIZE
            y0 = i * CELL_SIZE
            x1 = x0 + CELL_SIZE
            y1 = y0 + CELL_SIZE
            color = "black" if grid[i][j] == 1 else "white"
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="gray")


def main():
    grid = initialize_grid(GRID_SIZE, PROB_ALIVE)

    root = tk.Tk()
    root.title("Cellular Automaton")
    
    canvas = tk.Canvas(root, width=GRID_SIZE*CELL_SIZE, height=GRID_SIZE*CELL_SIZE, bg="white")

    canvas.pack()

    draw_grid(canvas, grid)
    root.mainloop()

if __name__ == "__main__":
    main()