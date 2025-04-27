import tkinter as tk
import random
import time


GRID_SIZE = 100
PROB_ALIVE = 0.5
MAX_GEN = 250
wrap = 'no'
root = tk.Tk()
gen = tk.IntVar(value=1)
play_pause_btn_text = tk.StringVar(value="Play 🎵")
continue_playing = False
selected_wrap = tk.StringVar(value='no')
selected_prob = tk.DoubleVar(value=0.5)
selected_glider = tk.BooleanVar(value=False)

def play_pause(grid, canvas, cell_size):
    global continue_playing
    if play_pause_btn_text.get() == "Play 🎵":
        play_pause_btn_text.set("Pause ⏸️")
        continue_playing = True;
        play_to_end(grid, canvas, cell_size)
    else:
        continue_playing = False;
        play_pause_btn_text.set("Play 🎵")


def play_to_end(grid, canvas, cell_size):
    global continue_playing
    global gen
    if gen.get() < MAX_GEN:
        if continue_playing:
            next_gen(grid, canvas, cell_size)
            canvas.update()
            canvas.after(5, play_to_end, grid, canvas, cell_size)
    else:
        continue_playing = False
        play_pause_btn_text.set("Play 🎵")

def next_gen(grid, canvas, cell_size):
    global gen, wrap
    wrap = selected_wrap.get()

    if gen.get() % 2 == 1:
        blue_step(grid)
    else:
        red_step(grid, wrap)
    draw_grid(canvas, grid, cell_size)
    gen.set(gen.get() + 1)


def back_gen(grid, canvas, cell_size):
    global gen, wrap
    wrap = selected_wrap.get()
    if gen.get() > 1:
        gen.set(gen.get() - 1)
        if gen.get() % 2 == 1:
            blue_step_b(grid)
        else:
            red_step_b(grid, wrap)
        draw_grid(canvas, grid, cell_size)

def get_b_values(grid, i, j):
    if wrap == 'yes':
        fixed_i_plus_one = i + 1
        fixed_j_plus_one = j + 1

        if (i + 1) == GRID_SIZE:
            fixed_i_plus_one = 0

        if (j + 1) == GRID_SIZE:
            fixed_j_plus_one = 0

        b1 = grid[i][j]
        b2 = grid[fixed_i_plus_one][j]
        b3 = grid[i][fixed_j_plus_one]
        b4 = grid[fixed_i_plus_one][fixed_j_plus_one]

    else:
        b1 = grid[i][j]
        b2 = grid[i + 1][j]
        b3 = grid[i][j + 1]
        b4 = grid[i + 1][j + 1]
    return b1, b2, b3, b4


def change_block_f(grid, i, j):
    b1, b2, b3, b4 = get_b_values(grid, i, j)
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


def change_block_b(grid, i, j):
    b1, b2, b3, b4 = get_b_values(grid, i, j)
    black = b1 + b2 + b3 + b4

    if black != 2:
        b1 = 1 - b1
        b2 = 1 - b2
        b3 = 1 - b3
        b4 = 1 - b4

        if black == 1:
            grid[i][j] = b4
            grid[i + 1][j] = b3
            grid[i][j + 1] = b2
            grid[i + 1][j + 1] = b1
        else:
            grid[i][j] = b1
            grid[i + 1][j] = b2
            grid[i][j + 1] = b3
            grid[i + 1][j + 1] = b4


def red_step(grid, wrap):
    for i in range(1, len(grid) -1, 2):
        for j in range(1, len(grid[0]) - 1, 2):
            change_block_f(grid, i, j)


def red_step_b(grid, wrap):
    for i in range(1, len(grid) -1, 2):
        for j in range(1, len(grid[0]) - 1, 2):
            change_block_b(grid, i, j)


def blue_step(grid):
    for i in range(0, len(grid) -1, 2):
        for j in range(0, len(grid[0]) - 1, 2):
            change_block_f(grid, i, j)


def blue_step_b(grid):
    for i in range(0, len(grid) -1, 2):
        for j in range(0, len(grid[0]) - 1, 2):
            change_block_b(grid, i, j)


def initialize_grid(size):
    global PROB_ALIVE
    PROB_ALIVE = selected_prob.get()

    return [
        [1 if random.random() < PROB_ALIVE else 0 for _ in range(size)]
        for _ in range(size)
    ]


def initialize_spiral_grid(size):
    grid = [[1 for _ in range(size)] for _ in range(size)]

    left_b = 1
    right_b = size - 2
    top_l = 1
    bottom_l = size - 2

    for i in range(left_b, right_b + 1):
        grid[top_l][i] = 0
        grid[bottom_l][i] = 0

    for i in range(top_l, bottom_l + 1):
        grid[i][left_b] = 0
        grid[i][right_b] = 0

    return grid


def initialize_spaced_spiral_grid(size):
    grid = [[0 for _ in range(size)] for _ in range(size)]

    left_b = 0
    right_b = size - 1
    top_l = 0
    bottom_l = size - 1

    while (left_b < right_b) and (top_l < bottom_l):
        for i in range(left_b, right_b + 1):
            grid[top_l][i] = 1
            grid[bottom_l][i] = 1

        for i in range(top_l, bottom_l + 1):
            grid[i][left_b] = 1
            grid[i][right_b] = 1

        top_l += 2
        bottom_l -= 2
        left_b += 2
        right_b -= 2

    return grid


def initialize_glider_grid(grid_size):
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    # Glider pattern (4x4)
    pattern = [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ]

    offset = grid_size // 2 - 2  # Center the pattern

    for i in range(4):
        for j in range(4):
            grid[offset + i][offset + j] = pattern[i][j]

    return grid


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


def start_simulation(grid, menu_frame):
    menu_frame.destroy()
    initialize_gui(grid)


def return_to_menu(root):
    global gen
    gen.set(1)
    for widget in root.winfo_children():
        widget.destroy()
    start_menu()


def start_menu():
    global PROB_ALIVE

    root.title("Cellular Automaton - Menu")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    adj_height = int(screen_height * 0.9)
    cell_size = min(screen_width // GRID_SIZE, adj_height // GRID_SIZE)
    canvas_width = cell_size * GRID_SIZE
    canvas_height = cell_size * GRID_SIZE
    total_width = canvas_width + 200
    root.geometry(f"{total_width}x{canvas_height}")

    menu_frame = tk.Frame(root, bg="#9BCD9B", bd=2, relief="ridge")
    menu_frame.pack(fill="both", expand=True)

    title = tk.Label(menu_frame, text="Welcome to Cellular Automaton!", font=("Arial", 20, "bold"), bg="#9BCD9B")
    title.pack(pady=30)

    settings_frame = tk.Frame(menu_frame, bg="#9BCD9B")
    settings_frame.pack(pady=10)

    wrap_label = tk.Label(settings_frame, text="Wrap Around:", font=("Arial", 14), bg="#9BCD9B")
    wrap_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    wrap_menu = tk.OptionMenu(settings_frame, selected_wrap, 'yes', 'no')
    wrap_menu.config(font=("Arial", 12), width=10)
    wrap_menu.grid(row=0, column=1, padx=10, pady=5)

    prob_label = tk.Label(settings_frame, text="Initial Probability:", font=("Arial", 14), bg="#9BCD9B")
    prob_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

    prob_menu = tk.OptionMenu(settings_frame, selected_prob, '0.25', '0.5', '0.75')
    prob_menu.config(font=("Arial", 12), width=10)
    prob_menu.grid(row=1, column=1, padx=10, pady=5)

    start_btn = tk.Button(menu_frame, text="Start Simulation", font=("Arial", 14, "bold"), bg="#008B00", fg="white",
                          width=20, command=lambda: start_simulation(initialize_grid(GRID_SIZE), menu_frame))
    start_btn.pack(pady=10)

    title2 = tk.Label(menu_frame, text="Special run options:", font=("Arial", 18, "bold"), bg="#9BCD9B")
    title2.pack(pady=20)

    glider_check = tk.Button(menu_frame, text="Start Glider Simulator", font=("Arial", 14),
                             command=lambda: start_simulation(initialize_glider_grid(GRID_SIZE), menu_frame))
    glider_check.pack(pady=20)

    start_special_btn = tk.Button(menu_frame, text="Start First Special Simulation",
                      font=("Arial", 14), command=lambda: start_simulation(initialize_spiral_grid(GRID_SIZE), menu_frame))
    start_special_btn.pack(pady=10)

    start_special2_btn = tk.Button(menu_frame, text="Start Second Special Simulation",
                      font=("Arial", 14),
                      command=lambda: start_simulation(initialize_spaced_spiral_grid(GRID_SIZE), menu_frame))
    start_special2_btn.pack(pady=10)

    exit_btn = tk.Button(menu_frame, text="Exit", font=("Arial", 14, "bold"), bg="#CD5555", fg="white", width=20,
                         command=root.quit)
    exit_btn.pack(pady=5)


def initialize_gui(grid):
    root.title("Cellular Automaton")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    adj_height = int(screen_height * 0.9)

    cell_size = min(screen_width // GRID_SIZE, adj_height // GRID_SIZE)

    canvas_width = cell_size * GRID_SIZE
    canvas_height = cell_size * GRID_SIZE

    root.geometry(f"{canvas_width + 200}x{canvas_height}")

    toolbar = tk.Frame(root, width=200, bg="#87CEEB")
    toolbar.pack(side="left", fill="y")

    button_style = {
        "font": ("Arial", 12),
        "width": 16,
        "bg": "#ffffff",
        "relief": "raised",
        "bd": 2
    }

    play_button = tk.Button(toolbar, textvariable=play_pause_btn_text,
                            command=lambda: play_pause(grid, canvas, cell_size),
                            **button_style)
    play_button.pack(pady=(20, 10))


    step_title_label = tk.Label(toolbar, text="Step:", font=("Arial", 12, "bold"), bg="#87CEEB")
    step_title_label.pack(pady=(10, 0))

    step_no_label = tk.Label(toolbar, textvariable=gen, font=("Arial", 12), bg="#87CEEB")
    step_no_label.pack(pady=(0, 10))


    next_button = tk.Button(toolbar, text="Next ⏭️",
                            command=lambda: next_gen(grid, canvas, cell_size),
                            **button_style)
    next_button.pack(pady=8)


    back_button = tk.Button(toolbar, text="Back ⏮️",
                            command=lambda: back_gen(grid, canvas, cell_size),
                            **button_style)
    back_button.pack(pady=8)

    separator = tk.Frame(toolbar, height=2, bd=1, relief="sunken", bg="#ccc")
    separator.pack(fill="x", padx=5, pady=12)


    menu_button = tk.Button(toolbar, text="Menu 🏠",
                            command=lambda: return_to_menu(root),
                            **button_style)
    menu_button.pack(pady=10)


    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="#87CEEB")
    canvas.pack(side="right", fill="both", expand=True)

    draw_grid(canvas, grid, cell_size)

    root.mainloop()


def main():
    start_menu()
    root.mainloop()

if __name__ == "__main__":
    main()