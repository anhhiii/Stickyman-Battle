from collections import deque
import heapq
import random
import math
import numpy as np

def bfs_path(start, goal, grid, margin_data=None, map_width=None, map_height=None):
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
            if (0 <= nx < cols and 0 <= ny < rows and not visited[ny][nx] and grid[ny][nx] == 0):
                # Kiểm tra margin
                if margin_data and map_width and map_height:
                    margin_index = ny * map_width + nx
                    if margin_index < len(margin_data) and margin_data[margin_index] != 0:
                        continue  # Bỏ qua ô có margin
                queue.append((nx, ny))
                visited[ny][nx] = True
                prev[ny][nx] = (x, y)

    path = []
    at = goal
    while at != start:
        path.append(at)
        at = prev[at[1]][at[0]]
        if at is None:
            return []
    path.reverse()
    return path

def greedy_path(start, goal, grid, margin_data=None, map_width=None, map_height=None):
    def manhattan_distance(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    prev = [[None for _ in range(cols)] for _ in range(rows)]
    pq = [(manhattan_distance(start, goal), start)]
    visited[start[1]][start[0]] = True
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while pq:
        _, (x, y) = heapq.heappop(pq)
        if (x, y) == goal:
            break
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < cols and 0 <= ny < rows and not visited[ny][nx] and grid[ny][nx] == 0):
                # Kiểm tra margin
                if margin_data and map_width and map_height:
                    margin_index = ny * map_width + nx
                    if margin_index < len(margin_data) and margin_data[margin_index] != 0:
                        continue
                heapq.heappush(pq, (manhattan_distance((nx, ny), goal), (nx, ny)))
                visited[ny][nx] = True
                prev[ny][nx] = (x, y)

    path = []
    at = goal
    while at != start:
        path.append(at)
        at = prev[at[1]][at[0]]
        if at is None:
            return []
    path.reverse()
    return path

def backtracking_path(start, goal, grid, margin_data=None, map_width=None, map_height=None):
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    path = []

    def dfs(x, y):
        if (x, y) == goal:
            path.append((x, y))
            return True
        visited[y][x] = True
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < cols and 0 <= ny < rows and not visited[ny][nx] and grid[ny][nx] == 0):
                # Kiểm tra margin
                if margin_data and map_width and map_height:
                    margin_index = ny * map_width + nx
                    if margin_index < len(margin_data) and margin_data[margin_index] != 0:
                        continue
                if dfs(nx, ny):
                    path.append((x, y))
                    return True
        return False

    dfs(start[0], start[1])
    path.reverse()
    return path

def and_or_search(start, goal, grid, margin_data=None, map_width=None, map_height=None):
    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    path = []

    def dfs(x, y, depth=0, max_depth=100):
        if depth > max_depth:
            return False
        if (x, y) == goal:
            path.append((x, y))
            return True
        visited[y][x] = True
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < cols and 0 <= ny < rows and not visited[ny][nx] and grid[ny][nx] == 0):
                # Kiểm tra margin
                if margin_data and map_width and map_height:
                    margin_index = ny * map_width + nx
                    if margin_index < len(margin_data) and margin_data[margin_index] != 0:
                        continue
                if dfs(nx, ny, depth + 1, max_depth):
                    path.append((x, y))
                    return True
        visited[y][x] = False
        return False

    dfs(start[0], start[1])
    path.reverse()
    return path

def hill_climb_step(current, goal, grid, margin_data=None, map_width=None, map_height=None):
    def manhattan_distance(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    best_score = manhattan_distance(current, goal)
    best_pos = current

    for dx, dy in directions:
        nx, ny = current[0] + dx, current[1] + dy
        if (0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 0):
            # Kiểm tra margin
            if margin_data and map_width and map_height:
                margin_index = ny * map_width + nx
                if margin_index < len(margin_data) and margin_data[margin_index] != 0:
                    continue
            score = manhattan_distance((nx, ny), goal)
            if score < best_score:
                best_score = score
                best_pos = (nx, ny)
    return best_pos

def q_learning_train(grid, start, goal, episodes=100, margin_data=None, map_width=None, map_height=None):
    rows, cols = len(grid), len(grid[0])
    actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # xuống, phải, lên, trái
    q_table = {}
    alpha, gamma, epsilon = 0.1, 0.9, 0.1

    def get_state(pos):
        return pos

    def get_valid_actions(state):
        x, y = state
        valid = []
        for dx, dy in actions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 0):
                # Kiểm tra margin
                if margin_data and map_width and map_height:
                    margin_index = ny * map_width + nx
                    if margin_index < len(margin_data) and margin_data[margin_index] != 0:
                        continue
                valid.append((dx, dy))
        return valid

    for _ in range(episodes):
        state = start
        while state != goal:
            state_key = get_state(state)
            if state_key not in q_table:
                q_table[state_key] = {action: 0 for action in actions}
            valid_actions = get_valid_actions(state)
            if not valid_actions:
                break
            if random.random() < epsilon:
                action = random.choice(valid_actions)
            else:
                action = max(valid_actions, key=lambda a: q_table[state_key].get(a, 0))
            dx, dy = action
            next_state = (state[0] + dx, state[1] + dy)
            reward = -1
            if next_state == goal:
                reward = 100
            next_state_key = get_state(next_state)
            if next_state_key not in q_table:
                q_table[next_state_key] = {action: 0 for action in actions}
            next_valid_actions = get_valid_actions(next_state)
            if next_valid_actions:
                next_max = max(q_table[next_state_key][a] for a in next_valid_actions)
            else:
                next_max = 0
            q_table[state_key][action] += alpha * (reward + gamma * next_max - q_table[state_key][action])
            state = next_state
    return q_table

def q_learning_step(current, q_table, grid, margin_data=None, map_width=None, map_height=None):
    rows, cols = len(grid), len(grid[0])
    actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # xuống, phải, lên, trái

    def get_state(pos):
        return pos

    def get_valid_actions(state):
        x, y = state
        valid = []
        for dx, dy in actions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 0):
                # Kiểm tra margin
                if margin_data and map_width and map_height:
                    margin_index = ny * map_width + nx
                    if margin_index < len(margin_data) and margin_data[margin_index] != 0:
                        continue
                valid.append((dx, dy))
        return valid

    state = get_state(current)
    if state not in q_table:
        q_table[state] = {action: 0 for action in actions}
    
    valid_actions = get_valid_actions(state)
    if not valid_actions:
        return current  # Trả về vị trí hiện tại nếu không có hành động hợp lệ

    # Chọn hành động tốt nhất từ Q-table
    best_action = max(valid_actions, key=lambda a: q_table[state].get(a, 0))
    dx, dy = best_action
    next_pos = (current[0] + dx, current[1] + dy)
    
    return next_pos