from lib.benchmark import time_benchmark
from lib.SearchAlgorithm import SearchAlgorithm

class BacktrackingSearch(SearchAlgorithm):
    def __init__(self, id, initial_state, goal_state):
        super().__init__(id, initial_state, goal_state)


    def _search(self):
        x, y = self._get_next_empty_cell()

        # no more empty cells
        if x == -1 and y == -1:
            if (self.current_state != self.goal_state): 
                # if answer found is not the same as goal_state, backtrack and find another answer
                return False
            else:
                # accept the answer
                self.completed = True
                return True
        
        # attempt from 1 - 9
        for i in range(1, 10):
            self.current_state[y][x] = i
            self.path_length += 1

            # if move is valid, continue with recursion. 
            if self._validate_sudoku_cell(x, y) and self._search():
                # solution found down this path, exiting the recursion stack
                return True
                
            #move not legal, backtrack and try another number for the cell
            self.current_state[y][x] = 0
            self.path_length += 1

        # none of the numbers attempted are valid, search failed
        return False


def main():
    sudoku_dataset = BacktrackingSearch.get_sudoku_dataset()
    for data in sudoku_dataset:
        BacktrackingSearch(data["id"], data["initial_state"], data["goal_state"])

    BacktrackingSearch.solve_all()


if __name__ == "__main__":
    main()
