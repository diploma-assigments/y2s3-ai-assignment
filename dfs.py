from lib.benchmark import time_benchmark
from lib.Solution import Solution
class DFS(Solution):
    def __init__(self):
        self.times = 0
        super().__init__()


    @time_benchmark
    def start(self):
        solving_board = self.dataset[17]["initial_state"]
        success = self.recursive_attempt(solving_board)
        print(f"is successful: {success}")


    def recursive_attempt(self, board):
        x, y = self.get_next_empty_cell(board)

        # no more empty cells
        if x == -1 and y == -1:
            return True
        
        # attempt from 1 - 9
        for i in range(1, 10):
            board[y][x] = i
            is_legal = self.validate_sudoku_cell(board, x, y)

            if is_legal:
                # if is legal, continue the path
                if self.recursive_attempt(board):
                    return True
                else:
                    # backtracked, try another number for the cell
                    board[y][x] = 0

        # none of the numbers attempted are valid, search failed
        return False

if __name__ == "__main__":
    DFS().start()
