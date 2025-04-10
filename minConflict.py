import random
import copy
from lib.SearchAlgorithm import SearchAlgorithm

class MinConflict(SearchAlgorithm):
    def __init__(self, id, initial_state, goal_state):
        super().__init__(id, copy.deepcopy(initial_state), goal_state)
        self.variables = []  # (x, y) tuples of initially empty cells
        self.allowed = {}    # Dict: (x, y) -> list of allowed values

        # get variables (initially empty cells)
        for y in range(9):
            for x in range(9):
                if self.current_state[y][x] == 0:
                    self.variables.append((x, y))

        # Precompute allowed values for each variable
        for (x, y) in self.variables:
            # get used numbers in row, column, box from initial_state (fixed cells)
            row = initial_state[y]
            column = [initial_state[i][x] for i in range(9)]
            box_x_start = (x // 3) * 3
            box_y_start = (y // 3) * 3
            box = []
            for i in range(box_y_start, box_y_start + 3):
                for j in range(box_x_start, box_x_start + 3):
                    box.append(initial_state[i][j])
            used = set(row) | set(column) | set(box)
            allowed_values = [num for num in range(1, 10) if num not in used]
            self.allowed[(x, y)] = allowed_values

        # Initialize variables with random allowed values
        for (x, y) in self.variables:
            if not self.allowed[(x, y)]:
                self.completed = False
                return
            self.current_state[y][x] = random.choice(self.allowed[(x, y)])

    def _search(self):
        max_steps = 100000  # can adjust based on problem difficulty
        for _ in range(max_steps):
            # check if current state is goal
            if self.current_state == self.goal_state:
                self.completed = True
                return True

            # Find all conflicting variables
            conflicting_vars = []
            for (x, y) in self.variables:
                current_value = self.current_state[y][x]
                conflict = False

                # Check row for conflicts with other variables
                for x2 in range(9):
                    if x2 == x:
                        continue
                    if (x2, y) in self.variables and self.current_state[y][x2] == current_value:
                        conflict = True
                        break
                if conflict:
                    conflicting_vars.append((x, y))
                    continue

                # Check column for conflicts with other variables
                for y2 in range(9):
                    if y2 == y:
                        continue
                    if (x, y2) in self.variables and self.current_state[y2][x] == current_value:
                        conflict = True
                        break
                if conflict:
                    conflicting_vars.append((x, y))
                    continue

                # Check box for conflicts with other variables
                box_x_start = (x // 3) * 3
                box_y_start = (y // 3) * 3
                for y2 in range(box_y_start, box_y_start + 3):
                    for x2 in range(box_x_start, box_x_start + 3):
                        if x2 == x and y2 == y:
                            continue
                        if (x2, y2) in self.variables and self.current_state[y2][x2] == current_value:
                            conflict = True
                            break
                    if conflict:
                        break
                if conflict:
                    conflicting_vars.append((x, y))

            # If no conflicting variables, check validity and compare to goal
            if not conflicting_vars:
                # Validate the entire Sudoku
                valid = True
                for y in range(9):
                    for x in range(9):
                        if not self._validate_sudoku_cell(x, y):
                            valid = False
                            break
                    if not valid:
                        break
                if valid and self.current_state == self.goal_state:
                    self.completed = True
                    return True
                else:
                    # no conflicts but not the solution, return fail
                    return False

            # Select a random conflicting variable
            var = random.choice(conflicting_vars)
            x, y = var
            current_value = self.current_state[y][x]

            # Evaluate each possible value for this variable to find the one with minimal conflicts
            min_conflicts = float('inf')
            best_value = current_value  # Default to current value if all else is equal
            for value in self.allowed[var]:
                if value == current_value:
                    continue  # skip current value to encourage change

                conflict_count = 0

                # Check row conflicts
                for x2 in range(9):
                    if x2 != x and (x2, y) in self.variables and self.current_state[y][x2] == value:
                        conflict_count += 1

                # Check column conflicts
                for y2 in range(9):
                    if y2 != y and (x, y2) in self.variables and self.current_state[y2][x] == value:
                        conflict_count += 1

                # Check box conflicts
                box_x_start = (x // 3) * 3
                box_y_start = (y // 3) * 3
                for y2 in range(box_y_start, box_y_start + 3):
                    for x2 in range(box_x_start, box_x_start + 3):
                        if (x2 != x or y2 != y) and (x2, y2) in self.variables and self.current_state[y2][x2] == value:
                            conflict_count += 1

                # Update best_value if this value has fewer conflicts or randomly choose in case of tie
                if conflict_count < min_conflicts or (conflict_count == min_conflicts and random.random() < 0.5):
                    min_conflicts = conflict_count
                    best_value = value

            # update the variable's value
            self.current_state[y][x] = best_value

        # max steps reached without finding a solution, fail
        return False

def main():
    sudoku_dataset = MinConflict.get_sudoku_dataset()
    for data in sudoku_dataset:
        MinConflict(data["id"], data["initial_state"], data["goal_state"])

    MinConflict.solve_all()

if __name__ == "__main__":
    main()