# Class to contain all functionality related to the GUI
import sys
import tkinter
from tkinter.ttk import Separator, Style
import SudokuSolver
import TempFolder

# static variables
new_grid = []
grid_choices = []
choices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
root = tkinter.Tk()

# Error message
error_message = tkinter.Label(root, text="Error, duplicated values found")
error_message.config(fg="red")
error_message.grid_remove()


def confirm():
    new_grid.clear()
    for choice in grid_choices:
        new_grid.append(int(choice.get()))

    if not SudokuSolver.check_grid(new_grid):
        error_message.grid(row=13, columnspan=11)
    else:
        root.destroy()


def close_box():
    TempFolder.remove_temp_folder()
    sys.exit()


# Create grid lines for the grid
def grid_lines(tk_root):
    # Create grid lines for the grid
    for a in range(11):
        # Vertical lines
        Separator(tk_root, orient="vertical").grid(column=3, row=a, sticky="ns")
        Separator(tk_root, orient="vertical").grid(column=7, row=a, sticky="ns")
        # Horizontal lines
        Separator(tk_root, orient="horizontal").grid(column=a, row=3, sticky="ew")
        Separator(tk_root, orient="horizontal").grid(column=a, row=7, sticky="ew")
    Style(tk_root).configure("TSeparator", background="red")


# Check to see if the grid is correct (tkinter gui)
def start_gui(grid):
    # Setting window size
    root.geometry("482x360")
    # Preventing the window from being resized
    root.resizable(width=False, height=False)
    # Setting window name
    root.title("Sudoku grid")

    # set up the drop down menus
    row_count = 0
    column_count = 0
    for grid_number in grid:
        choice = tkinter.StringVar(root)
        choice.set(grid_number)
        pop_up_menu = tkinter.OptionMenu(root, choice, *choices)
        grid_choices.append(choice)
        pop_up_menu.grid(row=row_count, column=column_count)

        # to accommodate for the red separator lines
        column_count += 1
        if column_count == 3 or column_count == 7:
            column_count += 1
        elif column_count % 11 == 0:
            row_count += 1
            column_count = 0
            if row_count == 3 or row_count == 7:
                row_count += 1

    # Create grid lines for the grid
    grid_lines(root)

    # Add message and button to confirm
    message = tkinter.Label(root, text="Make sure all the numbers are correct")
    message.grid(row=12, columnspan=7)

    confirm_button = tkinter.Button(root, text="Confirm", command=confirm)
    confirm_button.grid(row=12, column=8, columnspan=2)

    # Start the GUI
    root.protocol("WM_DELETE_WINDOW", close_box)
    root.mainloop()


# GUI to display the solution
def solution_gui(solved_grid):
    solution_root = tkinter.Tk()
    # Setting window size
    solution_root.geometry("240x290")
    # Preventing the window from being resized
    solution_root.resizable(width=False, height=False)
    # Setting window name
    solution_root.title("Sudoku solution grid")

    # GUI for if the grid could not be solved
    if isinstance(solved_grid, list):
        # set up the drop down menus
        row_count = 0
        column_count = 0
        for cell_digit in solved_grid:
            cell = tkinter.Label(solution_root, text=cell_digit)
            cell.grid(row=row_count, column=column_count, padx=5, pady=5)

            # to accommodate for the red separator lines
            column_count += 1
            if column_count == 3 or column_count == 7:
                column_count += 1
            elif column_count % 11 == 0:
                row_count += 1
                column_count = 0
                if row_count == 3 or row_count == 7:
                    row_count += 1

        # Create grid lines for the grid
        grid_lines(solution_root)
    else:
        message = tkinter.Label(solution_root, text=solved_grid)
        message.pack(pady=30)

    solution_root.protocol("WM_DELETE_WINDOW", close_box)
    solution_root.mainloop()
