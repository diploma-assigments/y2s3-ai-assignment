import json
import os

class Solution():
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), "sudoku_dataset.json")) as f:
            self.dataset = json.load(f)
        
    # check if a number is legal in the position
    def sudoku_validation(self, board: list[list[int]], x: int, y: int):
        # for storing checked values
        _ = set()

        # check x axis
        for value in board[y]:
            if value != 0 and value in _:
                return False
            _.add(value)

        _.clear()

        #check y axis
        for i in range(9):
            if board[i][x] != 0 and board[i][x] in _:
                return False
            _.add(board[i][x])

        _.clear()

        #check within box 
        box_root = { "x": (x // 3) * 3, "y": (y // 3) * 3 }
        for i in range (box_root["y"], box_root["y"] + 3):
            for j in range(box_root["x"], box_root["x"] + 3):
                if board[y][x] != 0 and board[y][x] in _: 
                    return False
                _.add(board[i][x])       

        return True