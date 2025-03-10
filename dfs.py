from lib.benchmark import time_benchmark
from lib.SearchAlgorithm import SearchAlgorithm

class DFS(SearchAlgorithm):
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
                return True
        
        # attempt from 1 - 9
        for i in range(1, 10):
            self.current_state[y][x] = i
            self.path_length += 1

            if self._validate_sudoku_cell(x, y):
                # legal, continue with next layer of recursion
                if self._search():
                    # backtracked, found a solution, end the recursion stack
                    return True
                else:
                    # backtracked, no solution found, try another number for the cell
                    self.current_state[y][x] = 0
                    self.path_length += 1
            else:
                #move not legal, backtrack immediately and try another number for the cell
                self.current_state[y][x] = 0
                self.path_length += 1

        # none of the numbers attempted are valid, search failed
        return False


def main():
    sudoku_dataset = SearchAlgorithm.get_sudoku_dataset()
    for data in sudoku_dataset:
        DFS(data["id"], data["initial_state"], data["goal_state"]).solve()

    SearchAlgorithm.wait_for_all_solves()


if __name__ == "__main__":
    main()
