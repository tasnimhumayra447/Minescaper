"""
Minescaper - A terminal-based Minesweeper variant
Author: Humayra Tasnim Nooha

Navigate from the top-left corner to the bottom-right exit
without stepping on any mines. Use WASD to move, append F to flag a cell.
You win if you reach the bottom-right cell and lose if you step on a mine.
"""


# ---------------------------------------------------------------------------
# Task 1: Mine board creation
# ---------------------------------------------------------------------------

def neighbouring_mines(x, y, grid_size, board):
    """Counts the number of mines adjacent to the cell (x, y) on the board.

    Args:
        x is an integer that is the row index of the cell.
        y is an integer that is the column index of the cell.
        grid_size is the size of the square board.
        board is a 2D list representing the board.
    Returns:
        The number of adjacent mines (0 to 8).
    """

    # initialise number of mines
    count = 0

    # Relative positions of 8 possible neighbours
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]

    # check if each neighbour is a mine
    for dx, dy in directions:
        new_x = x + dx
        new_y = y + dy

        # Ensure neighbour is within bounds
        if (0 <= new_x < grid_size) and (0 <= new_y < grid_size):
            if board[new_x][new_y] == -1:
                count += 1
    return count


def create_mine_board(grid_size, mine_positions):
    """Creates a mine board with -1 for mines and 0-8 for adjacent mine counts.

    Args:
        grid_size is an integer that represents size of the square board.
        mine_positions is a list of tuples where each tuple gives
            the (row, column) position of a mine.
    Returns:
        A 2D list representing the mine board.
    """
    
    # initialise the board with all zeros
    board = []
    for i in range(grid_size):
        board.append([0] * grid_size)

    # place mines; use a set for O(1) membership checks
    mine_set = set(mine_positions)
    for x, y in mine_set:
        board[x][y] = -1

    # don't allow mines at the top-left or bottom-right cells
    if board[0][0] == -1 or board[grid_size-1][grid_size-1] == -1:
        raise ValueError("Mine cannot be placed on the start or exit cell.") 

    # fill every non-mine cell with its adjacent mine count
    for x in range(grid_size):
        for y in range(grid_size):
            if board[x][y] != -1:
                board[x][y] = neighbouring_mines(x, y, grid_size, board)

    return board


# ---------------------------------------------------------------------------
# Task 2: Input processing
# ---------------------------------------------------------------------------

def process_input(mine_board, current_pos, move_str):
    """Processes a player's move and determines new position and flag status.
    
    Args:
        `mine_board` is a 2D list representing the mine_board.
        `current_pos` is a tuple showing player's current position.
        `move_str` is a string representing the player's move.
    Returns:
         a tuple (x, y, flag_cell), where (x, y) is the new position 
         and flag_cell is True if the cell was flagged, and False otherwise.
    """
    max_index = len(mine_board) - 1  # Largest valid index on the board
    new_pos = list(current_pos)  # Start with current position

    # Convert to uppercase and take up to the first 3 characters
    temp_str = move_str[:3].upper()

    # Remove invalid characters first
    cleaned = ""
    for char in temp_str:
        if char in "WASDF":
            cleaned += char

    # Flag is only valid as the final character
    flag = len(cleaned) >= 2 and cleaned[-1] == 'F'

    # Build directional move from everything before the trailing F
    processed_move = ""
    for char in cleaned:
        if char in "WASD":
            processed_move += char

    # Apply the move to new_pos
    steps_taken = 0
    for char in processed_move:
        # Must be directional move so stop after 2 steps
        if steps_taken < 2:
            if char == 'W':
                new_pos[0] -= 1
                steps_taken += 1
            elif char == "S":
                new_pos[0] += 1
                steps_taken += 1
            elif char == 'A':
                new_pos[1] -= 1
                steps_taken += 1
            elif char == "D":
                new_pos[1] += 1
                steps_taken += 1
        
    # if out-of-bounds move, reset new_pos
    if (not (0 <= new_pos[0] <= max_index) or not (0 <= new_pos[1] <= max_index)):
        new_pos = list(current_pos)
        flag = False
    
    # Cannot flag the start or end position
    if new_pos == [0, 0] or new_pos == [max_index, max_index]:
        flag = False
        
    return new_pos[0], new_pos[1], flag


# ---------------------------------------------------------------------------
# Task 3: Revealing connected zero cells
# ---------------------------------------------------------------------------

def reveal_zeros(mine_board, visited, current_pos):
    """Reveals all connected zero-value cells and their neighbours.

    Args:
        mine_board is a 2D list representing the mine_board.
        current_pos is a tuple showing player's current position.
        visited is a set of coordinate tuples (x, y) of
            previously visited cells.
    Returns:
        A set of (x, y) tuples of the original visited cells
        and any newly revealed ones.
    """

    # Mark current cell as visited
    visited.add(current_pos)

    x, y = current_pos
    max_index = len(mine_board) - 1  # Largest valid index on the board

    # cell has a non-zero count so stop recursion
    if mine_board[x][y] != 0:
        return visited

    # Relative positions of 8 possible neighbours
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy

        # check if neighbour is within bounds and not yet visited
        if (0 <= new_x <= max_index) and (0 <= new_y <= max_index):
            if (new_x, new_y) not in visited:
                reveal_zeros(mine_board, visited, (new_x, new_y))

    return visited


# ---------------------------------------------------------------------------
# Task 4: Game board rendering
# ---------------------------------------------------------------------------

def create_game_board(
        mine_board, 
        visited, 
        current_pos, 
        flagged, 
        show_all=False
):
    """Creates a game board based on the player's progress.

    Args:
        `mine_board` is a 2D list representing the mine_board.
        `visited` is a set of coordinate tuples (x, y) of 
            previously visited cells.
        `current_pos` is a tuple showing player's current position.
        `flagged` is a set of coordinate tuples (x, y) of 
            flagged cells. 
        `show_all` is a bool indicating whether the game has ended. 
    Returns:
         A 2D list representing the game board.
    """
    grid_size = len(mine_board)
    exit_pos = (grid_size - 1, grid_size - 1)

    # initialise game board with empty rows
    game_board = [[] for i in range(grid_size)]

    # game not over
    if not show_all:
        for x in range(grid_size):
            for y in range(grid_size):

                # current cell
                if (x, y) == current_pos:
                    game_board[x].append(f'[{mine_board[x][y]}]')

                # cell visited before
                elif (x, y) in visited:
                    game_board[x].append(f' {mine_board[x][y]} ')

                # flagged cell
                elif (x, y) in flagged:
                    game_board[x].append(' F ')

                # exit cell
                elif (x, y) == exit_pos:
                    game_board[x].append(' E ')

                # hidden unrevealed cell
                else:
                    game_board[x].append(' . ')
                    
    # game over
    else:
        for x in range(grid_size):
            for y in range(grid_size):

                # current cell
                if (x, y) == current_pos:
                    # current position is exit cell
                    if (x, y) == exit_pos:
                        game_board[x].append('[E]')
                    # current position is a mine
                    else:
                        game_board[x].append('[*]')

                # exit cell
                elif (x, y) == exit_pos:
                    game_board[x].append(' E ')

                # cell is not a mine
                elif mine_board[x][y] != -1:
                    game_board[x].append(f' {mine_board[x][y]} ')

                # cell is a mine
                else:
                    game_board[x].append(' * ')    
        
    return game_board


# ---------------------------------------------------------------------------
# Display helper
# ---------------------------------------------------------------------------

def print_game_board(game_board):
    """Prints the game board to the terminal in a readable grid format."""
    for row in game_board:
        print(" ".join(row))

