import copy
import json
import os

class Solution():
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), "sudoku_dataset.json")) as f:
            self.dataset = json.load(f)
        
        self.total_path_length = 0
        self.total_complete_solve = 0
        self.total_incomplete_solve = 0
        

    # return (x, y) of an empty cell from the board. returns (-1, -1) if no empty cell
    def get_next_empty_cell(self, board: list[list[int]]) -> tuple[int, int]:
        for y, row in enumerate(board):
            for x, value in enumerate(row):
                if value == 0:
                    return x, y
        return -1, -1


    # check if a number is legal in the position
    def validate_sudoku_cell(self, board: list[list[int]], x: int, y: int) -> bool:
        # copy from reference
        board_copy = copy.deepcopy(board)

        # get cell num out of board
        num = 0
        num, board_copy[y][x] = board_copy[y][x], num

        # check x axis
        if (num in board_copy[y]):
             return False

        #check y axis
        if (num in [board_copy[i][x] for i in range(9)]):
            return False

        #check within box 
        box_start_x = (x // 3) * 3
        box_start_y = (y // 3) * 3
        for i in range(box_start_y, box_start_y + 3):
            for j in range(box_start_x, box_start_x + 3):
                if board_copy[i][j] == num:
                    return False

        return True