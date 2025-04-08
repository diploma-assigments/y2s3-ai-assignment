import copy
import json
import os
import threading
import textwrap

from abc import abstractmethod
from time import time

class SearchAlgorithm():
    _problems: list["SearchAlgorithm"] = [] # TEMP?
    _threads = []
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
    def _problem_threading_wrapper(cls, problem):
        start_time = time()
        problem._search()
        problem.time_seconds_taken = round(time() - start_time, 4)
        cls._print_threading_status()

    @classmethod
    def _print_threading_status(cls):
        with cls._threading_lock:
            message = textwrap.dedent("""
            +--------------------------------------------------+
            | Problem |   Status   | Completeness | Time Taken |
            +---------+------------+--------------+------------+
            """)
            
            for problem in cls._problems:
                status = "running..." if problem.time_seconds_taken == 0 else "done!"
                completeness = "✅" if problem.completed else "❌"
                time_taken = f"{problem.time_seconds_taken:.4f}s" if problem.time_seconds_taken else "-"

                message += f"| {problem.id:<7} | {status:<10} | {completeness:<11} | {time_taken:<10} |\n"

            message += "+---------+------------+--------------+------------+"
            
            os.system("cls" if os.name == "nt" else "clear")
            print(message)


    @classmethod
    def solve_all(cls):
        """Run all problems with multiple threads, this function will block until all problems are solved."""
        for problem in cls._problems:
            t = threading.Thread(target=cls._problem_threading_wrapper, args=(problem,), daemon=True)
            t.start()
            cls._threads.append(t)
        
        try:
            for t in cls._threads:
                t.join()  # Wait for each thread to finish
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt detected! Exiting...")
            return
        

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
