# Class that contains the functions to solve the sudoku grid

import numpy

# Set up some static variables
boxes = []


# setting up the boxes (group the larger grid into the smaller grids)
def set_up_boxes():
    number_line = numpy.arange(81).reshape((9, 9))
    for hbox in numpy.hsplit(number_line, 3):
        for vbox in numpy.vsplit(hbox, 3):
            boxes.append(vbox.reshape(9))


# function to check the whole sudoku grid
def check_grid(grid):
    for x in range(81):
        if not check_cell(grid, x):
            return False
    return True


# Chek there are no duplicates in the grid
def check_cell(grid_as_row, cell):
    if not grid_as_row[cell] == 0:
        # Code to check columns
        column = cell % 9
        while column <= 80:
            if column != cell and grid_as_row[cell] == grid_as_row[column]:
                return False
            column += 9

        # Code to check rows
        row = cell - (cell % 9)
        for y in range(row, row + 8, 1):
            if y != cell and grid_as_row[y] == grid_as_row[cell]:
                return False

        for box in boxes:
            if cell in box:
                for z in box:
                    if cell != z and grid_as_row[cell] == grid_as_row[z]:
                        return False
    return True


# function to solve the grid
def solve_grid(grid):
    # setting the array of choices
    choices = numpy.arange(81, dtype=object)
    for a in range(81):
        if grid[a] != 0:
            choices[a] = [grid[a]]
        else:
            choices[a] = list(numpy.arange(1, 10, dtype=numpy.int8))

    # reduce the newly confirmed integers
    loop = True
    while loop:
        loop = False
        for e in range(81):
            if len(choices[e]) == 1:
                # Code to remove the same ints from columns
                column = e % 9
                while column <= 80:
                    if column != e and choices[e] in choices[column]:
                        choices[column].remove(choices[e])
                        loop = True
                    column += 9

                # Code to remove the same ints from rows
                row = e - (e % 9)
                for f in range(row, row + 8, 1):
                    if f != e and choices[e] in choices[f]:
                        choices[f].remove(choices[e])
                        loop = True

                # Code to remove the same ints from box
                for box in boxes:
                    if e in box:
                        for g in box:
                            if g != e and choices[e] in choices[g]:
                                choices[g].remove(choices[e])
                                loop = True

    # Back tracking
    cell = 0
    list_cell = 0
    grid_as_row_copy = grid
    while cell < 81:
        # set int
        grid_as_row_copy[cell] = choices[cell][list_cell]

        # check
        check = check_cell(grid_as_row_copy, cell)

        # if ok move to next cell
        if check:
            cell += 1
            list_cell = 0
        # if not then set int again
        elif list_cell < len(choices[cell]) - 1:
            list_cell += 1
        else:
            back_track = True
            while back_track:
                # if no more ints then back track
                grid_as_row_copy[cell] = 0
                cell -= 1

                if choices[cell].index(grid_as_row_copy[cell]) + 1 < len(choices[cell]):
                    list_cell = choices[cell].index(grid_as_row_copy[cell]) + 1
                    back_track = False

    # check the solution
    if check_grid(grid_as_row_copy):
        return grid_as_row_copy
    else:
        return 'Could not be solved \nusing back tracking'
