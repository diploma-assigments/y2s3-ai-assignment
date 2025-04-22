import math
import random
import copy
from lib.SearchAlgorithm import SearchAlgorithm

class SimulatedAnnealing(SearchAlgorithm):
    def __init__(self, id, initial_state, goal_state):
        super().__init__(id, copy.deepcopy(initial_state), goal_state)
        self.original_puzzle = copy.deepcopy(initial_state)
        self.side = len(initial_state)
        self.sq_size = int(math.sqrt(self.side))
        self.empty_cells = []
        self._initialize_puzzle()

        # Track best solution seen
        self.best_state = copy.deepcopy(self.current_state)
        self.best_energy = self._calculate_energy(self.current_state)

    def _initialize_puzzle(self):
        """Fill empty cells in each block with a random permutation of missing values"""
        self.empty_cells = []
        for block_idx in range(self.side):
            br = (block_idx // self.sq_size) * self.sq_size
            bc = (block_idx % self.sq_size) * self.sq_size
            present = []
            empties = []
            for i in range(self.sq_size):
                for j in range(self.sq_size):
                    y, x = br + i, bc + j
                    if self.original_puzzle[y][x] == 0:
                        empties.append((y, x))
                    else:
                        present.append(self.current_state[y][x])

            missing = list(set(range(1, self.side + 1)) - set(present))
            random.shuffle(missing)
            for (y, x), v in zip(empties, missing):
                self.current_state[y][x] = v

            if empties:
                self.empty_cells.append(empties)

    def _calculate_energy(self, state):
        """Count total row and column conflicts"""
        e = 0
        for row in state:
            e += len(row) - len(set(row))
        for col in zip(*state):
            e += len(col) - len(set(col))
        return e

    def _block_conflict(self, block):
        """Compute conflict score of a block to bias neighbor selection"""
        score = 0
        for y, x in block:
            val = self.current_state[y][x]
            # row conflicts
            score += self.current_state[y].count(val) - 1
            # column conflicts
            col = [r[x] for r in self.current_state]
            score += col.count(val) - 1
        return score

    def _generate_neighbor(self):
        """Swap two values in a conflict-prone block chosen proportionally to its conflicts"""
        new = copy.deepcopy(self.current_state)
        valid = [b for b in self.empty_cells if len(b) >= 2]
        if not valid:
            return new

        # weight blocks by current conflict
        weights = [self._block_conflict(b) + 1 for b in valid]
        block = random.choices(valid, weights=weights, k=1)[0]
        a, b = random.sample(block, 2)
        y1, x1 = a; y2, x2 = b
        new[y1][x1], new[y2][x2] = new[y2][x2], new[y1][x1]
        return new

    def _search(self):
        target = 0
        max_iter = 3_000_000
        initial_temp = 0.5
        stuck_thresh = 10_000
        hill_interval = 100_000
        hill_steps = 5_000
        reheat_blocks = True

        current_energy = self._calculate_energy(self.current_state)
        T = initial_temp
        stuck_count = 0
        self.path_length = 0

        # Precompute cooling schedule cutoff
        geo_cutoff = int(max_iter * 0.8)
        linear_rate = initial_temp / (max_iter - geo_cutoff)

        # Loop until max iterations or solution found
        while self.path_length < max_iter and current_energy > target:
            self.path_length += 1
            i = self.path_length

            # Smart reheating
            if stuck_count > stuck_thresh or T < 1e-5:
                T = initial_temp
                stuck_count = 0
                if reheat_blocks and self.empty_cells:
                    blk = random.choice(self.empty_cells)
                    vals = [self.current_state[y][x] for y, x in blk]
                    random.shuffle(vals)
                    for (y, x), v in zip(blk, vals):
                        self.current_state[y][x] = v
                    current_energy = self._calculate_energy(self.current_state)

            # Hybrid hill-climb bursts
            if i % hill_interval == 0:
                for _ in range(hill_steps):
                    nb = self._generate_neighbor()
                    e_nb = self._calculate_energy(nb)
                    if e_nb < current_energy:
                        self.current_state, current_energy = nb, e_nb
                        stuck_count = 0
                        if current_energy < self.best_energy:
                            self.best_energy = current_energy
                            self.best_state = copy.deepcopy(self.current_state)

            # Generate and maybe accept neighbor
            neighbor = self._generate_neighbor()
            e_n = self._calculate_energy(neighbor)
            delta = current_energy - e_n
            if delta > 0 or math.exp(delta / T) > random.random():
                self.current_state, current_energy = neighbor, e_n
                stuck_count = 0
                if current_energy < self.best_energy:
                    self.best_energy = current_energy
                    self.best_state = copy.deepcopy(self.current_state)
            else:
                stuck_count += 1

            # Cooling
            if i < geo_cutoff:
                T *= 0.999995
            else:
                T = max(0.0, T - linear_rate)

            # Diagnostics
            if i % 500_000 == 0:
                print(f"Iter {i:,}: E={current_energy}, best={self.best_energy}, T={T:.2e}")

        # Finalize
        self.current_state = self.best_state
        self.completed = (self.best_energy == target)
        return self.completed


def main():
    sudoku_dataset = SimulatedAnnealing.get_sudoku_dataset()
    for data in sudoku_dataset:
        SimulatedAnnealing(data['id'], data['initial_state'], data['goal_state'])
    SimulatedAnnealing.solve_all()

if __name__ == '__main__':
    main()
