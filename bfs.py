import copy

from lib.benchmark import time_benchmark
from lib.SearchAlgorithm import SearchAlgorithm

class BFS(SearchAlgorithm):
    def __init__(self, id, initial_state, goal_state):
        # queue the valid states
        self.queue = []
        super().__init__(id, initial_state, goal_state)


    def _search(self):
        # add initial state to the queue to start
        self.queue.append(copy.deepcopy(self.current_state))

        # while queue is populated
        while (len(self.queue)):
            # work on the first state in queue
            self.current_state = self.queue[0]
            x, y = self._get_next_empty_cell()

            # no more empty cells
            if x == -1 and y == -1:
                if (self.current_state != self.goal_state): 
                    # if answer found is not the same as goal_state, find another answer
                    self.queue.pop(0)
                    continue
                else:
                    # accept the answer
                    self.completed = True
                    return True
            
            # attempt from 1 - 9
            for i in range(1, 10):
                self.current_state[y][x] = i
                self.path_length += 1

                # if move is valid, save state to queue
                if self._validate_sudoku_cell(x, y):
                    self.queue.append(copy.deepcopy(self.current_state))

            self.queue.pop(0)
                

        # search failed
        return False


def main():
    sudoku_dataset = BFS.get_sudoku_dataset()
    for data in sudoku_dataset:
        BFS(data["id"], data["initial_state"], data["goal_state"])

    BFS.solve_all()


if __name__ == "__main__":
    main()
