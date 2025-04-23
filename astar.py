import heapq
import copy
from lib.SearchAlgorithm import SearchAlgorithm

class AStar(SearchAlgorithm):
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

        def get_mrv(board):
            # Create a list of empty cells and calculate the MRV (minimum remaining values)
            empty_cells = []
            for y in range(9):
                for x in range(9):
                    if board[y][x] == 0:
                        valid_values = self._get_valid_values(x, y, board)
                        empty_cells.append((x, y, len(valid_values)))
            # Sort by MRV (fewest valid values first)
            return sorted(empty_cells, key=lambda x: x[2])

        open_set = []
        heapq.heappush(open_set, (heuristic(self.current_state), self.current_state))
        g_costs = {tuple(map(tuple, self.current_state)): 0}

        while open_set:
            _, current_board = heapq.heappop(open_set)

            if is_goal_state(current_board):
                self.completed = True
                return True

            # Get the empty cells ordered by MRV
            empty_cells_by_mrv = get_mrv(current_board)

            # If there are empty cells to process, pick the one with the least valid options (MRV)
            if empty_cells_by_mrv:
                x, y, _ = empty_cells_by_mrv[0]  # Take the cell with the least options
            else:
                continue  # No empty cells, just continue (though this shouldn't happen here)

            for i in range(1, 10):
                self.path_length += 1
                new_board = copy.deepcopy(current_board)
                if self._validate_cell_with_board(x, y, new_board, i):
                    new_board[y][x] = i
                    options = len(self._get_valid_values(x, y, current_board))
                    new_g_cost = g_costs[tuple(map(tuple, current_board))] + (options / 9)
                    # new_g_cost = g_costs[tuple(map(tuple, current_board))] + 1.0 + (sum(row.count(0) for row in current_board) / 81)
                    new_board_tuple = tuple(map(tuple, new_board))

                    if new_board_tuple not in g_costs or new_g_cost < g_costs[new_board_tuple]:
                        g_costs[new_board_tuple] = new_g_cost
                        f_val = heuristic(new_board) + new_g_cost
                        heapq.heappush(open_set, (f_val, new_board))

        return False

    def _get_valid_values(self, x, y, board):
        # Returns a list of valid values (1-9) for the cell (x, y)
        valid_values = []
        for num in range(1, 10):
            if self._validate_cell_with_board(x, y, board, num):
                valid_values.append(num)
        return valid_values

    def _get_next_empty_cell_from_board(self, board):
        # Now unused since MRV is taking over the cell selection
        for y in range(9):
            for x in range(9):
                if board[y][x] == 0:
                    return x, y
        return -1, -1

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

# Main entry point
def main():
    sudoku_dataset = AStar.get_sudoku_dataset()
    for data in sudoku_dataset:
        AStar(data["id"], data["initial_state"], data["goal_state"])
    AStar.solve_all()

if __name__ == "__main__":
    main()