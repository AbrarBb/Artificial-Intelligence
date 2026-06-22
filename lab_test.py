import random
import time
from collections import deque

# ==========================
# Grid Environment
# ==========================
class GridEnvironment:
    def __init__(self, rows, cols, obstacle_ratio=0.25):
        self.rows = rows
        self.cols = cols
        self.start = (0, 0)
        self.goal = (rows - 1, cols - 1)

        # Create empty grid
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

        # Generate random obstacles
        total_cells = rows * cols
        obstacle_count = int(total_cells * obstacle_ratio)

        placed = 0
        while placed < obstacle_count:
            r = random.randint(0, rows - 1)
            c = random.randint(0, cols - 1)

            if (r, c) != self.start and (r, c) != self.goal:
                if self.grid[r][c] == 0:
                    self.grid[r][c] = 1
                    placed += 1

    def is_valid(self, position):
        r, c = position

        return (
            0 <= r < self.rows and
            0 <= c < self.cols and
            self.grid[r][c] == 0
        )

    # Perceive adjacent obstacles
    def perceive(self, position):
        r, c = position

        directions = {
            "UP": (-1, 0),
            "DOWN": (1, 0),
            "LEFT": (0, -1),
            "RIGHT": (0, 1)
        }

        obstacles = []

        for direction, (dr, dc) in directions.items():
            nr, nc = r + dr, c + dc

            if (
                0 <= nr < self.rows and
                0 <= nc < self.cols and
                self.grid[nr][nc] == 1
            ):
                obstacles.append(direction)

        return obstacles

    def get_neighbors(self, position):
        r, c = position

        moves = [
            (-1, 0),  # Up
            (1, 0),   # Down
            (0, -1),  # Left
            (0, 1)    # Right
        ]

        neighbors = []

        for dr, dc in moves:
            nr, nc = r + dr, c + dc

            if self.is_valid((nr, nc)):
                neighbors.append((nr, nc))

        return neighbors

    def display(self):
        print("\nGrid:")
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) == self.start:
                    print("S", end=" ")
                elif (r, c) == self.goal:
                    print("G", end=" ")
                elif self.grid[r][c] == 1:
                    print("X", end=" ")
                else:
                    print(".", end=" ")
            print()


# ==========================
# Breadth First Search
# ==========================
def bfs(env):
    start_time = time.perf_counter()

    queue = deque([(env.start, [env.start])])
    visited = set([env.start])

    expanded = 0

    while queue:
        current, path = queue.popleft()
        expanded += 1

        if current == env.goal:
            end_time = time.perf_counter()

            return {
                "path": path,
                "nodes_expanded": expanded,
                "path_length": len(path) - 1,
                "time": end_time - start_time
            }

        env.perceive(current)

        for neighbor in env.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    end_time = time.perf_counter()

    return {
        "path": None,
        "nodes_expanded": expanded,
        "path_length": 0,
        "time": end_time - start_time
    }


# ==========================
# Depth First Search
# ==========================
def dfs(env):
    start_time = time.perf_counter()

    stack = [(env.start, [env.start])]
    visited = set()

    expanded = 0

    while stack:
        current, path = stack.pop()

        if current in visited:
            continue

        visited.add(current)
        expanded += 1

        if current == env.goal:
            end_time = time.perf_counter()

            return {
                "path": path,
                "nodes_expanded": expanded,
                "path_length": len(path) - 1,
                "time": end_time - start_time
            }

        env.perceive(current)

        for neighbor in reversed(env.get_neighbors(current)):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

    end_time = time.perf_counter()

    return {
        "path": None,
        "nodes_expanded": expanded,
        "path_length": 0,
        "time": end_time - start_time
    }


# ==========================
# Main Program
# ==========================
if __name__ == "__main__":

    env = GridEnvironment(10, 10, obstacle_ratio=0.25)

    env.display()

    print("\n===== BFS =====")
    bfs_result = bfs(env)

    print("Path:", bfs_result["path"])
    print("Nodes Expanded:", bfs_result["nodes_expanded"])
    print("Path Length:", bfs_result["path_length"])
    print("Execution Time:", bfs_result["time"], "seconds")

    print("\n===== DFS =====")
    dfs_result = dfs(env)

    print("Path:", dfs_result["path"])
    print("Nodes Expanded:", dfs_result["nodes_expanded"])
    print("Path Length:", dfs_result["path_length"])
    print("Execution Time:", dfs_result["time"], "seconds")