from typing import List, Tuple, Optional
from lib.benchmark import time_benchmark
from lib.SearchAlgorithm import SearchAlgorithm

class DFS(SearchAlgorithm):
    def __init__(self, problem_id: int, initial_state: List[List[int]], goal_state: List[List[int]]):
        super().__init__(problem_id, initial_state, goal_state)
        self.backtracks = 0  # Track number of backtracking operations
    
    def _get_next_empty_cell(self) -> Optional[Tuple[int, int]]:
        for y in range(9):
            for x in range(9):
                if self.current_state[y][x] == 0:
                    return x, y
        return None
    
    def _validate_sudoku_cell(self, x: int, y: int, num: int) -> bool:

        # Check row
        if num in self.current_state[y]:
            return False
        
        # Check column
        if num in [self.current_state[row][x] for row in range(9)]:
            return False
        
        # Check 3x3 sub-grid
        start_x, start_y = 3 * (x // 3), 3 * (y // 3)
        for dy in range(3):
            for dx in range(3):
                if self.current_state[start_y + dy][start_x + dx] == num:
                    return False
        
        return True

    def _search(self) -> bool:
        empty_cell = self._get_next_empty_cell()

        # No more empty cells left
        if empty_cell is None:
            self.completed = self.current_state == self.goal_state
            return self.completed
        
        x, y = empty_cell

        # Attempt numbers 1-9 in a randomized order for better performance
        for num in self._get_candidate_numbers():
            if self._validate_sudoku_cell(x, y, num):
                self.current_state[y][x] = num
                self.path_length += 1

                if self._search():  
                    return True  # Solution found, exit recursion
                
                # Backtrack
                self.current_state[y][x] = 0  
                self.path_length += 1
                self.backtracks += 1

        return False  # No valid number found, search failed
    
    def _get_candidate_numbers(self) -> List[int]:
        import random
        nums = list(range(1, 10))
        random.shuffle(nums)
        return nums

    def solve(self) -> bool:
        try:
            result = self._search()
            print(f"Problem {self.id}: {'Solved' if result else 'Unsolvable'}")
            print(f"Path Length: {self.path_length}")
            print(f"Backtracks: {self.backtracks}")
            return result
        except Exception as e:
            print(f"Error solving problem {self.id}: {e}")
            return False

def main():
    sudoku_dataset = DFS.get_sudoku_dataset()
    problems = [DFS(data["id"], data["initial_state"], data["goal_state"]) for data in sudoku_dataset]
    for problem in problems:
        problem.solve()

    # Use time_benchmark for performance measurement
    time_benchmark(DFS.solve_all)

if __name__ == "__main__":
    main()