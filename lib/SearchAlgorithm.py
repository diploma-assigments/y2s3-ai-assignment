import atexit
import copy
import json
import os
import concurrent.futures
import threading

from abc import abstractmethod

class SearchAlgorithm():
    _problems: list["SearchAlgorithm"] = [] # TEMP?
    _futures = [] # TEMP?
    _threading_lock = threading.Lock()

    def __init__(self, id: int, initial_state: list[list[int]], goal_state: list[list[int]]):
        self.id: int = id
        self.current_state: list[list[int]] = initial_state
        self.goal_state: list[list[int]] = goal_state
        self.path_length: int = 0
        self.completed: bool = False
        self.time_seconds_taken: float = 0    

        SearchAlgorithm._problems.append(self)


    @classmethod
    def get_sudoku_dataset(cls):
        """Get sudoku dataset (id, initial_state, goal_state)."""
        with open(os.path.join(os.path.dirname(__file__), "sudoku_dataset.json")) as f:
            return json.load(f)
        

    @classmethod
    def _log_problem_future_status(cls, future):
        # TODO: make thread-safe + improve this shit
        with cls._threading_lock:
            message = ""
            for problem in cls._problems:
                message += f"#{problem.id} is {"✅" if problem.completed else "❌"}\n"
            os.system("cls")
            print(message)


    @classmethod
    def solve_all(cls):
        """Run all problems with multiple threads, this function will block until all problems are solved."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
            atexit.register(lambda: executor.shutdown(wait=False))

            for problem in cls._problems:    
                future = executor.submit(problem._search)
                future.add_done_callback(cls._log_problem_future_status)

                cls._futures.append(future)


    @abstractmethod
    def _search(self):
        """Your main entry point for search algorithm implementation."""
        pass


    def _get_next_empty_cell(self) -> tuple[int, int]:
        """Returns (x, y) of an empty cell from the board. Returns (-1, -1) if no empty cell."""
        for y, row in enumerate(self.current_state):
            for x, value in enumerate(row):
                if value == 0:
                    return x, y
        return -1, -1


    def _validate_sudoku_cell(self, x: int, y: int) -> bool:
        """Check if a number is legal in the position."""
        # copy from reference
        board_copy = copy.deepcopy(self.current_state)

        # get cell num out of board
        num = 0
        num, board_copy[y][x] = board_copy[y][x], num

        # check x axis
        if (num in board_copy[y]):
            return False

        #check y axis
        if (num in [board_copy[i][x] for i in range(9)]):
            return False

        #check within box 
        box_start_x = (x // 3) * 3
        box_start_y = (y // 3) * 3
        for i in range(box_start_y, box_start_y + 3):
            for j in range(box_start_x, box_start_x + 3):
                if board_copy[i][j] == num:
                    return False

        return True
