from collections import deque
import heapq
import random
def bfs_path(start, goal, grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    prev = [[None for _ in range(cols)] for _ in range(rows)]

    queue = deque()
    queue.append(start)
    visited[start[1]][start[0]] = True

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # xuống, phải, lên, trái

    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            break
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and not visited[ny][nx] and grid[ny][nx] == 0:
                queue.append((nx, ny))
                visited[ny][nx] = True
                prev[ny][nx] = (x, y)

    # Truy vết lại đường đi
    path = []
    at = goal
    while at != start:
        path.append(at)
        at = prev[at[1]][at[0]]
        if at is None:
            return []  # không tìm thấy đường đi
    path.reverse()
    return path


def greedy_path(start, goal, grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    parent = {}

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

    heap = [(heuristic(start, goal), start)]
    visited.add(start)

    while heap:
        _, current = heapq.heappop(heap)
        if current == goal:
            break
        x, y = current
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            neighbor = (nx, ny)
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 0 and neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                heapq.heappush(heap, (heuristic(neighbor, goal), neighbor))

    path = []
    current = goal
    while current != start:
        if current in parent:
            path.append(current)
            current = parent[current]
        else:
            return []  # không tìm được đường
    path.reverse()
    return path


def hill_climb_step(current, goal, grid):
    rows, cols = len(grid), len(grid[0])
    cx, cy = current
    gx, gy = goal

    best = current
    best_h = abs(cx - gx) + abs(cy - gy)

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = cx + dx, cy + dy
        if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 0:
            h = abs(nx - gx) + abs(ny - gy)
            if h < best_h:
                best = (nx, ny)
                best_h = h

    return best

def backtracking_path(start, goal, grid):
    path = []
    visited = set()

    def backtrack(pos):
        if pos == goal:
            path.append(pos)
            return True
        visited.add(pos)
        x, y = pos
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            next_pos = (nx, ny)
            if (0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and
                grid[ny][nx] == 0 and next_pos not in visited):
                if backtrack(next_pos):
                    path.append(pos)
                    return True
        return False

    if backtrack(start):
        path.reverse()
    return path

def q_learning_train(grid, start, goal, episodes=100, alpha=0.1, gamma=0.9, epsilon=0.1):
    rows, cols = len(grid), len(grid[0])
    q_table = {}
    actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def get_max_q(state):
        return max(q_table.get(state, {}).values(), default=0)

    for ep in range(episodes):
        state = start
        while state != goal:
            if state not in q_table:
                q_table[state] = {a: 0 for a in actions}

            if random.random() < epsilon:
                action = random.choice(actions)
            else:
                action = max(q_table[state], key=q_table[state].get)

            nx, ny = state[0] + action[0], state[1] + action[1]
            next_state = (nx, ny)

            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 0:
                reward = 100 if next_state == goal else -1
                if next_state not in q_table:
                    q_table[next_state] = {a: 0 for a in actions}
                q_table[state][action] += alpha * (reward + gamma * get_max_q(next_state) - q_table[state][action])
                state = next_state
            else:
                q_table[state][action] += alpha * (-5 - q_table[state][action])  # Phạt nếu đi vào tường

    return q_table

def q_learning_step(q_table, current):
    if current not in q_table:
        return current
    best_action = max(q_table[current], key=q_table[current].get)
    return (current[0] + best_action[0], current[1] + best_action[1])


def and_or_search(start, goal, grid):
    rows, cols = len(grid), len(grid[0])
    explored = set()
    plan = []

    def or_search(state, path):
        if state == goal:
            return []
        if state in path:
            return None

        for action in [(-1,0), (1,0), (0,-1), (0,1)]:
            next_state = (state[0]+action[0], state[1]+action[1])
            if 0 <= next_state[0] < cols and 0 <= next_state[1] < rows and grid[next_state[1]][next_state[0]] == 0:
                subplan = and_search(next_state, path + [state])
                if subplan is not None:
                    return [next_state] + subplan
        return None

    def and_search(state, path):
        return or_search(state, path)

    result = or_search(start, [])
    return result if result else []