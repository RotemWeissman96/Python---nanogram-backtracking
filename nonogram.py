#################################################################
# FILE : nonogram.py
# WRITERS : Nir Ayalon and , Rotem weissman
# EXERCISE : intro2cs2 ex8 2021
# DESCRIPTION: A backtracking program thats solves nonograms
# STUDENTS WE DISCUSSED THE EXERCISE WITH: None.
# WEB PAGES I USED:
# NOTES: If the function row variation returns a list with all the options to
# fill up row/ column, and in a specific cell all the option are -1 (that
# means that I don't know what to insert) and 1 for example.
# so I know that I don't have any option that leads me to insert 0.
# Thus the only option is 1, and the same goes if we got only -1's and 0's.
# Therefore we choose to return 0/1 in that case.
#################################################################


def _compare_items_in_lst(lst):
    """
   The function gets a list of 0,1,-1 and compares all the items in list,
   in order to determine what is the agreeable value to return. for example
   if all the items in list are the same it will return their value. If
   there is a disagreement (list that contains 0's and 1's) it will return
   -1.
   :param lst: (list) list of 0,1,-1
   :return: (int) 0/1/-1 the agreeable value, depends on the item in list
   """
    if len(lst) == 1:
        return lst[0]

    num_equals = 0
    indicator = -1
    for item in lst:
        if item != -1:
            indicator = item
            break
    if indicator == -1:
        return -1

    if indicator == 0:
        if 1 in lst:
            return -1
        else:
            return 0

    else:
        if 0 in lst:
            return -1
        else:
            return 1


def intersection_row(rows):
    """
    the function gets list of lists (rows) as an input and returns the
    one row (a list) that shares the common restrictions to all rows.

    :param rows: (list of lists)
    :return: (list) a row that shares the common restrictions
    """

    intersection = []
    if rows == []:  # recursion base1
        return intersection
    if len(rows) == 1:  # recursion base2
        return rows[0]
    else:
        for i in range(len(rows[0])):
            temp_lst = []
            for row in rows:
                temp_lst.append(row[i])
            intersection.append(_compare_items_in_lst(temp_lst))
            # appends(1/0/-1)
        return intersection


def create_board(constrains):
    """"
    The function build a two dimensional board (list of lists) that contain
    only -1.
    :param constrains (list of lists) our constrains
    :return board (list of lists) our board game
    """
    num_rows = len(constrains[0])
    num_cols = len(constrains[1])
    board = []
    for i in range(num_rows):
        board.append([])
        for j in range(num_cols):
            board[i].append(-1)
    return board


def get_column(board, index):
    """
    The function get and index of column in the board an extract all the
    items in that column into a list.
    :param board: (list of lists) our nonogram board
    :param index: (int) column number
    :return: new_row (list) list of all items in the chosen column
    """
    new_row = []
    for row in board:
        new_row.append(row[index])
    return new_row


def insert_column(column, index, board):
    """
    The function gets a list of items and changes the chosen column in the
    board by a given column number (index).
    :param column: (list) list of 0/1/-1
    :param index: (int) the number of column in the board we want to change
    the column
    :param board: (list of lists) our board
    :return: None
    """
    for i in range(len(board)):
        board[i][index] = column[i]


def _append_filled_white(final_list, current_row):
    """
    fills the row with white spaces (0) and append the row into final list
    :param final_list: saves all the valid rows
    :param current_row: the current row
    :return:
    """
    new_row = current_row[:]
    for i in range(len(current_row)):
        if current_row[i] == -1:
            new_row[i] = 0
    final_list.append(new_row)


def _sum_blocks(blocks):
    """
    calculate the minimum row size needed to fit the block list
    :param blocks: the block list
    :return: sum of all blocks and white spaces between blocks
    """
    if not blocks:  # if there are no blocks
        return 0
    summ = len(blocks) - 1  # adds all the white spaces between blocks
    for i in blocks:  # adds all the blocks
        summ += i
    return summ


def _fill_full_block(n, current_row, block):
    """
    appends a block in a row
    :param n: length of empty space in row
    :param current_row: the current row
    :param block: the block to add
    :return: None
    """
    for j in range(block):  # adds the block
        current_row.append(1)
    if block < n:  # if the row has an empty space after the block, add "0"
        current_row.append(0)


def _pop_full_block(current_row, block):
    """
    removes from the current row the last block that was added
    :param current_row: the current row
    :param block: the block size to remove
    :return: None
    """
    if current_row[-1] == 0:  # if the last number in the row is "0"
        current_row.pop()
    for j in range(block):  # removes the block from row
        current_row.pop()


def _constraint_satisfactions_helper(n, blocks, seq_list, current_row):
    """
    finds all the possible positions for the blocks in an n sized array
    uses recurtion and backtracking
    :param n: the size of the row
    :param blocks: list of all the block's length
    :param seq_list: saves all the valid rows
    :param current_row: calculate the current row and appends to seq_list
    after matching all the conditions
    :return: the list of all valid rows
    """
    if n <= 0 and not blocks:
        # base case: if block list is empty and row is finished
        seq_list.append(current_row[:])
    elif not blocks:
        # base case: if block list is empty and row is not finished
        for i in range(n):
            current_row.append(0)
        seq_list.append(current_row[:])
        for i in range(n):
            current_row.pop()
    else:
        if _sum_blocks(blocks) <= n - 1:
            # if there's' space in (row len-1) to fit all the remaining blocks
            current_row.append(0)
            _constraint_satisfactions_helper(n - 1, blocks, seq_list,
                                             current_row)
            current_row.pop()  # pop out the "0" added after recursive call
        _fill_full_block(n, current_row, blocks[0])
        _constraint_satisfactions_helper(n - blocks[0] - 1, blocks[1:],
                                         seq_list, current_row)
        _pop_full_block(current_row, blocks[0])
        # pop out the last inserted block after recursive call
    return seq_list


def constraint_satisfactions(n, blocks):
    """
    finds all the possible positions for the blocks in an n sized array
    uses the _constraint_satisfactions_helper functions
    :param n: row length
    :param blocks: list of blocks sizes
    :return: list of all possible positions for the blocks in the row
    """
    for i in blocks:
        if i <= 0:
            return []
    if n < _sum_blocks(blocks) or n <= 0:
        return []
    elif not blocks:
        return [0 for i in range(n)]
    else:
        return _constraint_satisfactions_helper(n, blocks[:], [], [])


def _can_continue(index, blocks, current_row):
    """
    check if the remaining of the current row is capable of appending the
    rest of the blocks
    :param index: the current index the recursion is at
    :param blocks: the remaining blocks to insert
    :param current_row: the current row to check
    :return: True if the current row is able to append the blocks and False
    if not
    """
    if _sum_blocks(blocks) > len(current_row) - index or index > \
            len(current_row) - 1:
        # check if there is space to append all the remaining blocks
        return False
    return True


def _check_block(blocks, index, current_row):
    """
    checks if the next block in block list can fin in current row
    :param blocks: the block list to enter the row
    :param index: the current index (in current_row) the recursion is at
    :param current_row: the current row to check
    :return: True if the next block fits or False if it doesnt
    """
    if index + blocks[0] > len(current_row):  # if the block is too long
        return False
    for i in range(blocks[0]):  # checks if there is 0 in the middle of block
        if current_row[index + i] == 0:
            return False
    if index + blocks[0] < len(current_row):
        if current_row[index + blocks[0]] == 1:
            # if there is "1" instead of "0" at the end of the block
            return False
        if len(blocks) == 1 and 1 in current_row[index + blocks[0]:]:
            # if this is the last block and there are more blocks ahead
            return False
    return True


def _insert_block(start_row, blocks, index, current_row, final_list):
    """
    inserts the next block to the current row and calls the correct next
    recursion of row_variations_helper, based on whether the block is at the
    end of the row or not
    :param start_row: the starting row, used to call the next recursion
    :param blocks: list of blocks to insert the row
    :param index: the current index (in current_row) the recursion is at
    :param current_row: the current row to check
    :param final_list: the final list of valid rows
    :return: None
    """
    for i in range(blocks[0]):  # inserts the block
        current_row[index + i] = 1
    if index + blocks[0] < len(current_row):  # if 0 is needed after the block
        current_row[index + blocks[0]] = 0
        row_variations_helper(start_row, blocks[1:], index + blocks[0] + 1,
                              current_row, final_list)
    else:
        row_variations_helper(start_row, blocks[1:], index + blocks[0],
                              current_row, final_list)


def row_variations_helper(start_row, blocks, index, current_row, final_list):
    """
    return all the possible row based on a starting row full of 1,-1,
    0 and blocks list. recursively checks validity of all options
    :param start_row: the row that was inserted initially
    :param blocks: the list of blocks remaining to check
    :param index: the place in the current row that the function checks
    :param current_row: the current row checked after changes the function made
    :param final_list: list of all the options for the row
    :return: final_list
    """
    if not blocks:  # if there are no more blocks
        _append_filled_white(final_list, current_row)
    elif not _can_continue(index, blocks, current_row):
        # if there is not enough space to enter the blocks in the row
        return final_list
    elif current_row[index] == 0:
        row_variations_helper(start_row, blocks, index + 1, current_row,
                              final_list)
    elif current_row[index] == 1:
        if _check_block(blocks, index, current_row):
            _insert_block(start_row, blocks, index, current_row, final_list)
        else:
            return final_list
    elif current_row[index] == -1:
        # if "-1" check it both with "0" and with "1"
        current_row[index] = 0
        row_variations_helper(start_row, blocks, index + 1, current_row,
                              final_list)
        current_row[index] = 1
        row_variations_helper(start_row, blocks, index, current_row,
                              final_list)
    current_row[index:] = start_row[index:]  # backtracking
    return final_list


def row_variations(row, blocks):
    """
    return all the possible row based on a starting row full of 1,-1,
    0 and blocks list. uses the recursive method row_variations_helper
    :param row: the row to insert all blocks
    :param blocks: the blocks to insert the row
    :return: list of all the options for the row
    """
    if not blocks and 1 in row:
        return []
    return row_variations_helper(row, blocks[:], 0, row[:], [])


def _change_rows(board, constraints, last_change):
    """
    change the board according to its rows and the rows constraints
    :param board: the board
    :param constraints: the constraints
    :param last_change: last changed index, used to break the loop in time
    :return: last changed row number, False if a full cycle with no change
    has been made, "not possible" if the board is impossible to solve
    """
    index = 0
    for i in range(len(board)):  # going through all rows first
        index = index + 1
        if index == last_change:
            return False
        potential_row = intersection_row(row_variations(board[i],
                                                        constraints[0][i]))
        if potential_row == []:  # if there are no options for row
            return "not possible"
        if potential_row != board[i]:  # if there is change to imply
            board[i] = potential_row[:]
            last_change = index
    return last_change


def _change_columns(board, constraints, last_change):
    """
    change the board according to its columns and the column's constraints
    :param board: the board
    :param constraints: the constraints
    :param last_change: last changed index, used to break the loop in time
    :return: last changed columns number, False if a full cycle with no change
    has been made, "not possible" if the board is impossible to solve
    """
    if last_change == False or last_change == "not possible":
        return last_change
    index = len(board)
    for i in range(len(board[0])):  # going through all columns
        index = index + 1
        if index == last_change:
            return False
        col = intersection_row(row_variations(get_column(board, i),
                                              constraints[1][i]))
        if col == []:  # when the intersection is empty
            return "not possible"
        if col != get_column(board, i):
            insert_column(col, i, board)
            last_change = index
    return last_change


def _solve_nonogram_round(board, constraints):
    """
    solve nonogram puzzle with 1 solution, by going repeatedly over all rows
    and all columns of constraints
    :param board: the solutions board, can be already not empty (-1)
    :param constraints: a list of list of blocks to insert the board
    :return: the best solution it can find or None if the game is impossible
    """
    last_change = -1
    # saves the last change index in order to break the while loop as soon
    # as no changes been made for a full loop, starts with the last
    while last_change:
        last_change = _change_rows(board, constraints, last_change)
        last_change = _change_columns(board, constraints, last_change)
        if last_change == "not possible":
            return []
        elif not last_change:
            break
    return board


def _change_rows_easy(board, constraints, last_change):
    """
    change the board according to its rows and the rows constraints
    :param board: the board
    :param constraints: the constraints
    :param last_change: last changed index, used to break the loop in time
    :return: last changed row number, False if a full cycle with no change
    has been made, "not possible" if the board is impossible to solve
    """
    index = 0
    for i in range(len(board)):  # going through all rows first
        index = index + 1
        if index == last_change:
            return False
        if -1 in board[i]:
            potential_row = intersection_row(row_variations(board[i],
                                                            constraints[0][i]))
            if potential_row == []:  # if there are no options for row
                return "not possible"
            if potential_row != board[i]:  # if there is change to imply
                board[i] = potential_row[:]
                last_change = index
    return last_change


def _change_columns_easy(board, constraints, last_change):
    """
     change the board according to its columns and the column's constraints
     :param board: the board
     :param constraints: the constraints
     :param last_change: last changed index, used to break the loop in time
     :return: last changed columns number, False if a full cycle with no change
     has been made, "not possible" if the board is impossible to solve
     """
    if last_change == False or last_change == "not possible":
        return last_change
    index = len(board)
    for i in range(len(board[0])):  # going through all columns
        index = index + 1
        if index == last_change:
            return False
        col = get_column(board, i)
        if -1 in col:
            col = intersection_row(row_variations(col, constraints[1][i]))
            if col == []:  # when the intersection is empty
                return "not possible"
            if col != get_column(board, i):
                insert_column(col, i, board)
                last_change = index
    return last_change


def solve_easy_nonogram(constraints):
    """
    solve nonogram puzzle from empty board, by going repeatedly over all
    rows and all columns of constraints matching them to the board
    :param constraints: a list of list of blocks to insert the board
    :return: the best solution it can find or None if the game is impossible
    """
    board = create_board(constraints)
    if board == []: return board
    last_change = -1
    # saves the last change index in order to break the while loop as soon
    # as no changes been made for a full loop, starts with the last
    while last_change:
        last_change = _change_rows(board, constraints, last_change)
        last_change = _change_columns(board, constraints, last_change)
        if last_change == "not possible":
            return None
        elif not last_change or last_change == -1:
            break
    return board


def _solve_nonogram_helper(board, constrains, index, solutions_lst):
    """
    Recursive function that uses backtracking to find solutions.
    :param board: (list of lists) our board game
    :param constrains:(list of lists) blocks to insert the board
    :param index: (int) tha cell index in the board
    :param solutions_lst: (list) final solutions list
    :return: solutions_lst (lst)
    """
    if not board:
        return
    length = len(constrains[0])
    width = len(constrains[1])
    if index == length * width - 1:
        solutions_lst.append(board)  # recursion base
        return
    col = index % width
    row = index // width
    if board[row][col] == -1:
        board[row][col] = 0  # recursion step
        new_board = _solve_nonogram_round(board, constrains)
        _solve_nonogram_helper(new_board, constrains, index + 1, solutions_lst)
        board[row][col] = 1  # recursion step
        new_board = _solve_nonogram_round(board, constrains)
        _solve_nonogram_helper(new_board, constrains, index + 1, solutions_lst)
        board[row][col] = -1
    else:
        for i in range(index, length * width):
            col = i % width
            row = i // width
            if board[row][col] == -1:
                index = i
                break
        else:
            index = length * width - 1
        _solve_nonogram_helper(board, constrains, index, solutions_lst)
    return solutions_lst


def solve_nonogram(constrains):
    """
    The function gets board constrains and returns a list of all possible
    solutions to the game
    :param constrains: (list of lists) row and columns constrains
    :return: solutions_lst (list) list of all possible solutions
    """
    board = solve_easy_nonogram(constrains)
    if board == []:
        return [[]]
    solutions_lst = []
    if board:
        index = 0
        _solve_nonogram_helper(board, constrains, index, solutions_lst)
    return solutions_lst

