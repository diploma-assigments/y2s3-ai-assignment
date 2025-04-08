from lib.benchmark import time_benchmark
from lib.SearchAlgorithm import SearchAlgorithm
import copy
import heapq

class GBFS(SearchAlgorithm):

    def __init__(self, id, initial_state, goal_state):
        super().__init__(id, initial_state, goal_state)


    def solve_sudoku(self, id, data):
        completed, path_length = self._GBFS(data["initial_state"])
        if completed:
            self.total_path_length += path_length
            self.total_complete_solve += 1
            print(f"Sudoku #{id} completed with {path_length} steps")
        else:
            self.total_incomplete_solve += 1
            print(f"Sudoku #{id} did not complete with {path_length} steps")
    


    def _GBFS(self, board):
        """ Greedy Best-First Search for Sudoku with proper heuristic """

        def _get_valid_values(board, x, y):
            """ Get valid numbers for a given cell """
            used = set(board[y])  # Row values
            used.update(board[i][x] for i in range(9))  # Column values

            # 3x3 Grid values
            box_x, box_y = (x // 3) * 3, (y // 3) * 3
            for i in range(3):
                for j in range(3):
                    used.add(board[box_y + i][box_x + j])

            return [num for num in range(1, 10) if num not in used]



        def _find_best_empty_cell(board):
            """ Find the empty cell with the fewest possible valid numbers (heuristic) """
            min_options = float('inf')
            best_cell = (-1, -1)
            best_values = []

            for y in range(9):
                for x in range(9):
                    if board[y][x] == 0:  # Empty cell
                        possible_values = _get_valid_values(board, x, y)
                        if len(possible_values) < min_options:
                            min_options = len(possible_values)
                            best_cell = (x, y)
                            best_values = possible_values

            return best_cell, best_values



        def is_solved(board):
            """ Check if the board is solved (no empty cells) """
            return all(all(cell != 0 for cell in row) for row in board)
        
        def compute_heuristic(board):
            score = 0
            for y in range(9):
                for x in range(9):
                    if board[y][x] == 0:
                        score += len(_get_valid_values(board, x, y))
            return score

        # Priority queue for GBFS
        queue = []
        heapq.heappush(queue, (0, board))  # Start with initial state (priority=0)

        visited = set()
        step_count = 0

        while queue:
            _, current_board = heapq.heappop(queue)  # Get the best heuristic state
            step_count += 1

            if is_solved(current_board):
                return current_board, step_count  # Solution found

            (x, y), valid_values = _find_best_empty_cell(current_board)
            if x == -1:
                continue  # No more moves

            for value in valid_values:
                new_board = copy.deepcopy(current_board)
                new_board[y][x] = value
                board_tuple = tuple(map(tuple, new_board))  # Convert to hashable type

                if board_tuple not in visited:
                    visited.add(board_tuple)
                    heapq.heappush(queue, (compute_heuristic(new_board), new_board))

        return None, step_count  # No solution found
    

def main():
    sudoku_dataset = GBFS.get_sudoku_dataset()
    for data in sudoku_dataset:
        GBFS(data["id"], data["initial_state"], data["goal_state"])
    GBFS.solve_all()

if __name__ == "__main__":
    main()