import tkinter as tk
import random
import time


GRID_SIZE = 100 # The number of cells in each row/column
PROB_ALIVE = 0.5 # The probability that a square in the grid would receive the "alive" (1) score
MAX_GEN = 250 # The maximum number of generations that would be shown when clicking "play"
wrap = 'no' # Will be "yes" when wraparound will be enabled
root = tk.Tk() # The base object of the GUI
gen = tk.IntVar(value=1) # The current generation number

play_pause_btn_text = tk.StringVar(value="Play 🎵") # The text currently displayed on the play/pause button
continue_playing = False # Will be "true" when the animation should be played
selected_wrap = tk.StringVar(value='no')
selected_prob = tk.DoubleVar(value=0.5)
selected_glider = tk.BooleanVar(value=False)

def play_pause(grid, canvas, cell_size):
    """
    Responsible to start / stop the animation and change the play/pause button's text accordingly
    :param grid: A two-dimensional array representing the values in the grid
    :param canvas: The GUI "canvas" object the grid is drawn on
    :param cell_size: The number of cels in each row/column of the grid
    """
    global continue_playing
    if play_pause_btn_text.get() == "Play 🎵":
        play_pause_btn_text.set("Pause ⏸️")
        continue_playing = True;
        play_to_end(grid, canvas, cell_size)
    else:
        continue_playing = False;
        play_pause_btn_text.set("Play 🎵")


def play_to_end(grid, canvas, cell_size):
    """
    Plays the animation forward while the current generation did not reach 250 and while the user has not
    requested the animation to be paused
    :param grid: A two-dimensional array representing the values in the grid
    :param canvas: The GUI "canvas" object the grid is drawn on
    :param cell_size: The number of cels in each row/column of the grid
    :return:
    """
    global continue_playing
    global gen
    if gen.get() < MAX_GEN:
        if continue_playing:
            next_gen(grid, canvas, cell_size)
            canvas.update()
            canvas.after(20, play_to_end, grid, canvas, cell_size)
            # Causes the next iteration of the canvas update to be called
    else:
        continue_playing = False
        play_pause_btn_text.set("Play 🎵")

def next_gen(grid, canvas, cell_size):
    """
    Moves the grid a generation forward. Carries out a "blue step" or a "red step" according to the number
    of the current generation
    :param grid: A two-dimensional array representing the values in the grid
    :param canvas: The GUI "canvas" object the grid is drawn on
    :param cell_size: The number of cels in each row/column of the grid
    """
    global gen, wrap
    wrap = selected_wrap.get()

    if gen.get() % 2 == 1:
        blue_step(grid)
    else:
        red_step(grid)
    draw_grid(canvas, grid, cell_size)
    gen.set(gen.get() + 1)


def back_gen(grid, canvas, cell_size):
    """
    Moves the grid a generation *backward*. Cancels the effects of the previous "blue step" or a "red step" according
    to the number of the current generation.
    :param grid: A two-dimensional array representing the values in the grid
    :param canvas: The GUI "canvas" object the grid is drawn on
    :param cell_size: The number of cels in each row/column of the grid
    """
    global gen, wrap
    wrap = selected_wrap.get()
    if gen.get() > 1:
        gen.set(gen.get() - 1)
        if gen.get() % 2 == 1:
            blue_step_b(grid)
        else:
            red_step_b(grid)
        draw_grid(canvas, grid, cell_size)


def change_block_f(grid, i, j):
    N = len(grid)
    M = len(grid[0])

    i1 = i % N
    i2 = (i + 1) % N
    j1 = j % M
    j2 = (j + 1) % M

    b1 = grid[i1][j1]
    b2 = grid[i2][j1]
    b3 = grid[i1][j2]
    b4 = grid[i2][j2]
    black = b1 + b2 + b3 + b4

    if black != 2:
        b1 = 1 - b1
        b2 = 1 - b2
        b3 = 1 - b3
        b4 = 1 - b4

        if black == 3:
            grid[i1][j1] = b4
            grid[i2][j1] = b3
            grid[i1][j2] = b2
            grid[i2][j2] = b1
        else:
            grid[i1][j1] = b1
            grid[i2][j1] = b2
            grid[i1][j2] = b3
            grid[i2][j2] = b4


def change_block_b(grid, i, j):
    """
    Changes the values of the four squares within a specified "block" in order to go a generation *backwards*.
    :param grid: A two-dimensional array representing the values in the grid
    :param i: The row index of the upper-left square of the grid
    :param j: The column index of the upper-left square of the grid
    :return: Nothing, this is a void function
    """
    N = len(grid)
    M = len(grid[0])

    i1 = i % N
    i2 = (i + 1) % N
    j1 = j % M
    j2 = (j + 1) % M

    b1 = grid[i1][j1]
    b2 = grid[i2][j1]
    b3 = grid[i1][j2]
    b4 = grid[i2][j2]
    black = b1 + b2 + b3 + b4

    if black != 2:
        b1 = 1 - b1
        b2 = 1 - b2
        b3 = 1 - b3
        b4 = 1 - b4

        if black == 1:
            grid[i][j] = b4
            grid[fixed_i_plus_one][j] = b3
            grid[i][fixed_j_plus_one] = b2
            grid[fixed_i_plus_one][fixed_j_plus_one] = b1
        elif black in (0, 3, 4):
            grid[i][j] = b1
            grid[fixed_i_plus_one][j] = b2
            grid[i][fixed_j_plus_one] = b3
            grid[fixed_i_plus_one][fixed_j_plus_one] = b4


def red_step(grid):
    """
    Forwards the grid data with a "red step" (a generational change based on blocks specified by the "red" lines)
    """
    if wrap == 'no':
        for i in range(1, len(grid) - 1, 2):
            for j in range(1, len(grid) - 1, 2):
                change_block_f(grid, i, j)
    else:
        for i in range(1, len(grid), 2):
            for j in range(1, len(grid), 2):
                change_block_f(grid, i, j)


def red_step_b(grid):
    """
    "Cancels" the effect of a "red step"
    """
    if wrap == 'no':
        for i in range(1, len(grid) - 1, 2):
            for j in range(1, len(grid) - 1, 2):
                change_block_b(grid, i, j)
    else:
        for i in range(1, len(grid), 2):
            for j in range(1, len(grid), 2):
                change_block_b(grid, i, j)


def blue_step(grid):
    """
    Forwards the grid data with a "blue step" (a generational change based on blocks specified by the "blue" lines)
    """
    for i in range(0, GRID_SIZE, 2):
        for j in range(0, GRID_SIZE, 2):
            change_block_f(grid, i, j)


def blue_step_b(grid):
    """
    "Cancels" the effect of a "blue step"
    """
    for i in range(0, GRID_SIZE - 1, 2):
        for j in range(0, GRID_SIZE - 1, 2):
            change_block_b(grid, i, j)


def initialize_grid(size):
    """
    Initializes the "grid" array so the "0" and "1" values would be initialized as per the probability the user
    chose for them in the menu screen
    """
    global PROB_ALIVE
    PROB_ALIVE = selected_prob.get()

    return [
        [1 if random.random() < PROB_ALIVE else 0 for _ in range(size)]
        for _ in range(size)
    ]

    return grid


def initialize_spiral_grid(size):
    """
    Initializes the "grid" array so a "frame" would be created on screen.
    As generations pass, a spiral shape would be created on screen.
    """
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
    """
    Initializes the "grid" array so spaced "frames" would be created on screen.
    As generations pass, a spiral shape would be created on screen.
    """
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
    """
    Initializes the "grid" array so a glider object will be created
    """

def initialize_glider_grid(grid_size):
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    # Define the 4x4 "bow and arrow" shape
    pattern = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0]
    ]

    pattern_height = len(pattern)
    pattern_width = len(pattern[0])
    min_gap = 8  # Minimum horizontal gap between patterns

    # Fixed vertical offset (starting row index)
    offset_y = 1

    # Iterate horizontally with gap
    for offset_x in range(0, grid_size - pattern_width + 1, pattern_width + min_gap):
        for i in range(pattern_height):
            for j in range(pattern_width):
                if offset_y + i < grid_size and offset_x + j < grid_size:
                    grid[offset_y + i][offset_x + j] = pattern[i][j]

    return grid


def draw_grid(canvas, grid, cell_size):
    """
    Draws a grid object on the screen based on the "grid" two-dimensional array
    """
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
    """
    Gets the user to the grid screen. The grid is drawn (or re-drawn) according to the parameters
    specified in the menu screen.
    """
    menu_frame.destroy()
    initialize_main_screen(grid)


def return_to_menu(root):
    """
    Returns the user to the menu screen from the grid screen. The current state of the grid is removed,
    so when re-entering the grid screen, it will be re-initialized.
    """
    global gen
    gen.set(1)
    for widget in root.winfo_children():
        widget.destroy()
    start_menu()


def start_menu():
    """
    Sets up the menu screen (in which the user chooses the parameters by which the grid would be initialized)
    """
    global PROB_ALIVE

    root.title("Cellular Automaton - Menu")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    adj_height = int(screen_height * 0.7)
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


def initialize_main_screen(grid):
    """
    Initializes the "grid" screen, which will display the current state of the grid and will enables the user
    to see how it changes generation by generation
    :param grid: A two-dimensional array representing the values in the grid
    """
    root.title("Cellular Automaton")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    adj_height = int(screen_height * 0.7)

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
    """
    Starts the program. The screen that will be displayed first would be the menu screen.
    """
    start_menu()
    root.mainloop()


if __name__ == "__main__":
    main()