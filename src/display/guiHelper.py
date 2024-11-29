"""Helper functions for developing GUIs"""

def populateGrid(grid, items):
    row_idx = 0
    col_idx = 0

    for item in items:
        grid.addWidget(item, row_idx, col_idx)

        # Figure out where to put the next element
        on_right_side = ((col_idx + 1) == grid.columnCount())
        on_bottom = ((row_idx +1) == grid.rowCount())

        if on_right_side and on_bottom:
            # We are on the corner and the grid is full. Determine which direction to expand
            if grid.columnCount() == grid.rowCount():
                # Grid is a square so expand right
                col_idx += 1
                row_idx = 0
            elif grid.columnCount() > grid.rowCount():
                # grid is a rectangle with columns having more elements so expand down
                col_idx = 0
                row_idx += 1
            else:
                # Should never get here.
                assert False
        elif on_right_side:
            # grid is not full and we are on the right side so expand down
            row_idx += 1
        elif on_bottom:
            # grid is not full and we are on the bottom so expand right
            col_idx += 1