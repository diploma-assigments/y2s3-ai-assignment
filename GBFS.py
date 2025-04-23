import heapq
import copy
from lib.SearchAlgorithm import SearchAlgorithm

class GBFS(SearchAlgorithm):
    def __init__(self, id, initial_state, goal_state):
        super().__init__(id, initial_state, goal_state)

    def _search(self):
        def heuristic(board):
            total_options = 0
            for y in range(9):
                for x in range(9):
                    if board[y][x] == 0:
                        options = 0
                        for num in range(1, 10):
                            if self._validate_cell_with_board(x, y, board, num):
                                options += 1
                        total_options += options
            return total_options

        def is_goal_state(board):
            return board == self.goal_state

        open_set = []
        heapq.heappush(open_set, (heuristic(self.current_state), self.current_state))

        while open_set:
            _, current_board = heapq.heappop(open_set)

            if is_goal_state(current_board):
                self.completed = True
                return True

            x, y = self._get_mrv_cell(current_board)
            if x == -1 and y == -1:
                continue

            for i in range(1, 10):
                self.path_length += 1
                new_board = copy.deepcopy(current_board)
                if self._validate_cell_with_board(x, y, new_board, i):
                    new_board[y][x] = i
                    heapq.heappush(open_set, (heuristic(new_board), new_board))

        return False

    def _get_mrv_cell(self, board):
        min_options = 10
        best_cell = (-1, -1)
        for y in range(9):
            for x in range(9):
                if board[y][x] == 0:
                    options = 0
                    for num in range(1, 10):
                        if self._validate_cell_with_board(x, y, board, num):
                            options += 1
                    if 0 < options < min_options:
                        min_options = options
                        best_cell = (x, y)
        return best_cell

    def _validate_cell_with_board(self, x, y, board, num):
        if num in board[y]:
            return False
        if num in [board[i][x] for i in range(9)]:
            return False
        box_x = (x // 3) * 3
        box_y = (y // 3) * 3
        for i in range(box_y, box_y + 3):
            for j in range(box_x, box_x + 3):
                if board[i][j] == num:
                    return False
        return True

def main():
    sudoku_dataset = GBFS.get_sudoku_dataset()
    for data in sudoku_dataset:
        GBFS(data["id"], data["initial_state"], data["goal_state"])
    GBFS.solve_all()

if __name__ == "__main__":
    main()