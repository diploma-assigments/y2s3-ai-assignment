import heapq
import copy
from lib.benchmark import time_benchmark
from lib.Solution import Solution

## IGNORE
class AStar(Solution):
    def __init__(self):
        super().__init__()

    @time_benchmark
    def start(self):
        for i, data in enumerate(self.dataset):
            self.solve_sudoku(i + 1, data)

    def solve_sudoku(self, id, data):
        completed, path_length = self.a_star_search(data["initial_state"])
        if completed:
            self.total_path_length += path_length
            self.total_complete_solve += 1
            print(f"Sudoku #{id} completed with {path_length} steps")
        else:
            self.total_incomplete_solve += 1
            print(f"Sudoku #{id} did not complete with {path_length} steps")

    def a_star_search(self, board):
        def heuristic(board):
            return sum(row.count(0) for row in board)

        def get_neighbors(board):
            neighbors = []
            x, y = self.get_next_empty_cell(board)
            if x == -1 and y == -1:
                return neighbors
            for i in range(1, 10):
                new_board = copy.deepcopy(board)
                new_board[y][x] = i
                if self.validate_sudoku_cell(new_board, x, y):
                    neighbors.append(new_board)
            return neighbors

        open_set = []
        heapq.heappush(open_set, (heuristic(board), 0, board))
        came_from = {}
        g_score = {str(board): 0}
        f_score = {str(board): heuristic(board)}

        while open_set:
            _, current_g, current = heapq.heappop(open_set)
            if heuristic(current) == 0:
                return True, current_g

            for neighbor in get_neighbors(current):
                tentative_g_score = current_g + 1
                neighbor_str = str(neighbor)
                if tentative_g_score < g_score.get(neighbor_str, float('inf')):
                    came_from[neighbor_str] = current
                    g_score[neighbor_str] = tentative_g_score
                    f_score[neighbor_str] = tentative_g_score + heuristic(neighbor)
                    heapq.heappush(open_set, (f_score[neighbor_str], tentative_g_score, neighbor))

        return False, g_score.get(str(board), 0)

if __name__ == "__main__":
    AStar().start()