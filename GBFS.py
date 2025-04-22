import copy
import heapq
from lib.SearchAlgorithm import SearchAlgorithm

class GBFS(SearchAlgorithm):


    def __init__(self, id, initial_state, goal_state):
        super().__init__(id, initial_state, goal_state)


    def _search(self):
        def heuristic(board):
            empty_cells = sum(row.count(0) for row in board)
            conflicts = 0
            for y in range(9):
                for x in range(9):
                    if board[y][x] != 0:
                        num = board[y][x]
                        board[y][x] = 0
                        if not self._validate_cell_with_board(x, y, board, num):
                            conflicts += 1
                        board[y][x] = num
            return empty_cells + conflicts

        def is_goal_state(board):
            return board == self.goal_state

        open_set = []
        # we push only h(n) (heuristic) in the open set
        heapq.heappush(open_set, (heuristic(self.current_state), self.current_state))
        visited = set()

        while open_set:
            # We pop only the heuristic value h(n) and the board
            _, current_board = heapq.heappop(open_set)

            if is_goal_state(current_board):
                self.completed = True
                return True

            board_tuple = tuple(map(tuple, current_board))
            if board_tuple in visited:
                continue
            visited.add(board_tuple)

            x, y = self._get_next_empty_cell_from_board(current_board)
            if x == -1 and y == -1:
                continue

            # For each possible number, create new board states and add them to open set
            for i in range(1, 10):
                new_board = copy.deepcopy(current_board)
                self.path_length += 1
                if self._validate_cell_with_board(x, y, new_board, i):
                    new_board[y][x] = i
                    # Push only the heuristic value to the open set modified
                    fn = heuristic(new_board) # f(n) = h(n) should be ok already dy
                    heapq.heappush(open_set, (fn, new_board))
                    

        return False
    
    def _get_next_empty_cell_from_board(self, board):
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


def main():
    sudoku_dataset = GBFS.get_sudoku_dataset()
    for data in sudoku_dataset:
        GBFS(data["id"], data["initial_state"], data["goal_state"])
    GBFS.solve_all()

if __name__ == "__main__":
    main()