from lib.benchmark import time_benchmark
from lib.Solution import Solution

class DFS(Solution):
    def __init__(self):
        super().__init__()


    @time_benchmark
    def start(self):
        for i, data in enumerate(self.dataset):
            self.solve_sudoku(i + 1, data)


    def solve_sudoku(self, id, data):
        completed, path_length = self.recursive_attempt(data["initial_state"], 0)
        if completed:
            # TODO: compare with goal state?
            self.total_path_length += path_length
            self.total_complete_solve += 1
            print(f"Sudoku #{id} completed with {path_length} steps")
        else:
            self.total_incomplete_solve += 1
            print(f"Sudoku #{id} did not complete with {path_length} steps")



    def recursive_attempt(self, board, path_length):
        x, y = self.get_next_empty_cell(board)

        # no more empty cells
        if x == -1 and y == -1:
            return True, path_length
        
        # attempt from 1 - 9
        for i in range(1, 10):
            board[y][x] = i
            path_length += 1

            if self.validate_sudoku_cell(board, x, y):
                # if is legal, continue the path
                solved, new_path_length = self.recursive_attempt(board, path_length)
                if solved:
                    return True, new_path_length
                else:
                    # backtracked from future path, try another number for the cell
                    board[y][x] = 0
                    path_length = new_path_length + 1
            else:
                #backtrack immediately and try another number for the cell
                board[y][x] = 0
                path_length += 1

        # none of the numbers attempted are valid, search failed
        return False, path_length

if __name__ == "__main__":
    DFS().start()
