import random
import copy
from lib.SearchAlgorithm import SearchAlgorithm

class MinConflict(SearchAlgorithm):
    def __init__(self, id, initial_state, goal_state):
        super().__init__(id, copy.deepcopy(initial_state), goal_state)
        self.variables = []  # List of (x, y) for initially empty cells
        self.allowed = {}    # (x, y) -> list of allowed values based on initial state

        # Identify variables (empty cells)
        for y in range(9):
            for x in range(9):
                if self.current_state[y][x] == 0:
                    self.variables.append((x, y))

        # Precompute allowed values per variable based on initial board
        for (x, y) in self.variables:
            used = set(self._get_row(initial_state, y)) | \
                   set(self._get_col(initial_state, x)) | \
                   set(self._get_box(initial_state, x, y))
            self.allowed[(x, y)] = [num for num in range(1, 10) if num not in used]

        # Randomly initialize each variable with an allowed value
        for (x, y) in self.variables:
            if not self.allowed[(x, y)]:
                self.completed = False
                return
            self.current_state[y][x] = random.choice(self.allowed[(x, y)])

    def _search(self):
        max_steps = 100000
        for _ in range(max_steps):
            conflicts = [
                (x, y) for (x, y) in self.variables
                if self._count_conflicts(x, y, self.current_state[y][x]) > 0
            ]

            if not conflicts:
                self.completed = True
                return True

            x, y = random.choice(conflicts)
            best_value = self.current_state[y][x]
            min_conflict = float("inf")

            for val in self.allowed[(x, y)]:
                if val == self.current_state[y][x]:
                    continue
                count = self._count_conflicts(x, y, val)
                if count < min_conflict or (count == min_conflict and random.random() < 0.5):
                    min_conflict = count
                    best_value = val

            self.current_state[y][x] = best_value

        return False

    def _get_row(self, board, y):
        return board[y]

    def _get_col(self, board, x):
        return [board[i][x] for i in range(9)]

    def _get_box(self, board, x, y):
        box_x = (x // 3) * 3
        box_y = (y // 3) * 3
        return [
            board[j][i]
            for j in range(box_y, box_y + 3)
            for i in range(box_x, box_x + 3)
        ]

    def _count_conflicts(self, x, y, value):
        count = 0
        # Row
        for i in range(9):
            if i != x and self.current_state[y][i] == value:
                count += 1
        # Column
        for i in range(9):
            if i != y and self.current_state[i][x] == value:
                count += 1
        # Box
        box_x = (x // 3) * 3
        box_y = (y // 3) * 3
        for j in range(box_y, box_y + 3):
            for i in range(box_x, box_x + 3):
                if (i != x or j != y) and self.current_state[j][i] == value:
                    count += 1
        return count

# Main function to solve all Sudoku puzzles in the dataset
def main():
    sudoku_dataset = MinConflict.get_sudoku_dataset()
    for data in sudoku_dataset:
        MinConflict(data["id"], data["initial_state"], data["goal_state"])
    MinConflict.solve_all()

if __name__ == "__main__":
    main()