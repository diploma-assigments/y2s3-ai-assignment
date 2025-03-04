board = [
    [4, 0, 3, 0, 2, 0, 0, 7, 1],
    [2, 6, 0, 0, 5, 0, 0, 4, 9],
    [9, 0, 8, 4, 0, 0, 0, 5, 6],
    [0, 4, 2, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 9, 1, 5],
    [1, 0, 9, 5, 0, 0, 0, 0, 7],
    [3, 8, 0, 2, 0, 9, 7, 0, 0],
    [0, 2, 1, 0, 3, 0, 5, 0, 8],
    [7, 9, 0, 0, 0, 0, 0, 0, 0]
]

board[0][1] = 5

def validate_sudoku_cell(board: list[list[int]], x: int, y: int) -> bool:
        # for storing checked values
        _ = set()

        # check x axis
        for value in board[y]:
            if value != 0 and value in _:
                return "False1"
            _.add(value)

        _.clear()

        #check y axis
        for i in range(9):
            if board[i][x] != 0 and board[i][x] in _:
                return "False2"
            _.add(board[i][x])

        _.clear()

        #check within box 
        box_start_row = (y // 3) * 3
        box_start_col = (x // 3) * 3
        for i in range(box_start_row, box_start_row + 3):
            for j in range(box_start_col, box_start_col + 3):
                value = board[i][j]
                if value != 0 and value in _:
                    return "False3"
                _.add(value)
            return True


result = validate_sudoku_cell(board, 1, 0)
print(result)