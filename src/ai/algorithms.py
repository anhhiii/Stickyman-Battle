from collections import deque
import heapq
import random

def bfs_path(start_id, goal_id, graph):  # graph là instance của PlatformGraph
    if start_id not in graph.nodes or goal_id not in graph.nodes:
        return []

    visited = set()
    queue = deque([[start_id]])

    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == goal_id:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.edges.get(node, []):
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
    return []

   
def greedy_path(start, goal, graph, is_platform=False, nodes=None):
    if is_platform:
        def heuristic(a, b):
            ax, ay = nodes[a]['center']
            bx, by = nodes[b]['center']
            return abs(ax - bx) + abs(ay - by)
        visited = set()
        parent = {}
        heap = [(heuristic(start, goal), start)]
        visited.add(start)
        while heap:
            _, current = heapq.heappop(heap)
            if current == goal:
                break
            for neighbor in graph.get(current, []):
                if neighbor not in visited:
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
                print(f"[Greedy] No path found from {start} to {goal}")
                return []
        path.reverse()
        print(f"[Greedy] Found path: {path}")
        return path
    else:
        rows, cols = len(graph), len(graph[0])
        visited = set()
        parent = {}
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
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
                if 0 <= nx < cols and 0 <= ny < rows and graph[ny][nx] == 0 and neighbor not in visited:
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
                print(f"[Greedy] No path found from {start} to {goal}")
                return []
        path.reverse()
        print(f"[Greedy] Found path: {path}")
        return path

def hill_climb_step(current, goal, graph, is_platform=False, nodes=None):
    if is_platform:
        def heuristic(a, b):
            ax, ay = nodes[a]['center']
            bx, by = nodes[b]['center']
            return abs(ax - bx) + abs(ay - by)
        best = current
        best_h = heuristic(current, goal)
        for neighbor in graph.get(current, []):
            h = heuristic(neighbor, goal)
            if h < best_h:
                best = neighbor
                best_h = h
        print(f"[Hill Climb] From {current} to {goal}, next step: {best}")
        return best
    else:
        rows, cols = len(graph), len(graph[0])
        cx, cy = current
        gx, gy = goal
        best = current
        best_h = abs(cx - gx) + abs(cy - gy)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < cols and 0 <= ny < rows and graph[ny][nx] == 0:
                h = abs(nx - gx) + abs(ny - gy)
                if h < best_h:
                    best = (nx, ny)
                    best_h = h
        print(f"[Hill Climb] From {current} to {goal}, next step: {best}")
        return best

def backtracking_path(start, goal, graph, is_platform=False, nodes=None):
    if is_platform:
        path = []
        visited = set()
        def backtrack(pos):
            if pos == goal:
                path.append(pos)
                return True
            visited.add(pos)
            for neighbor in graph.get(pos, []):
                if neighbor not in visited:
                    if backtrack(neighbor):
                        path.append(pos)
                        return True
            return False
        if backtrack(start):
            path.reverse()
            print(f"[Backtracking] Found path: {path}")
        else:
            print(f"[Backtracking] No path found from {start} to {goal}")
        return path
    else:
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
                if (0 <= nx < len(graph[0]) and 0 <= ny < len(graph) and
                    graph[ny][nx] == 0 and next_pos not in visited):
                    if backtrack(next_pos):
                        path.append(pos)
                        return True
            return False
        if backtrack(start):
            path.reverse()
            print(f"[Backtracking] Found path: {path}")
        else:
            print(f"[Backtracking] No path found from {start} to {goal}")
        return path

def q_learning_train(graph, start, goal, episodes=200, alpha=0.1, gamma=0.9, epsilon=0.1, is_platform=False, nodes=None):
    if is_platform:
        q_table = {}
        def get_neighbors(state):
            return graph.get(state, [])
        def get_max_q(state):
            return max(q_table.get(state, {}).values(), default=0)
        for ep in range(episodes):
            state = start
            while state != goal:
                if state not in q_table:
                    q_table[state] = {n: 0 for n in get_neighbors(state)}
                if random.random() < epsilon:
                    action = random.choice(get_neighbors(state))
                else:
                    action = max(q_table[state], key=q_table[state].get) if q_table[state] else random.choice(get_neighbors(state))
                next_state = action
                reward = 100 if next_state == goal else -1
                if next_state not in q_table:
                    q_table[next_state] = {n: 0 for n in get_neighbors(next_state)}
                q_table[state][action] += alpha * (reward + gamma * get_max_q(next_state) - q_table[state][action])
                state = next_state
        print(f"[Q-Learning] Trained Q-table: {q_table}")
        return q_table
    else:
        rows, cols = len(graph), len(graph[0])
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
                if 0 <= nx < cols and 0 <= ny < rows and graph[ny][nx] == 0:
                    reward = 100 if next_state == goal else -1
                    if next_state not in q_table:
                        q_table[next_state] = {a: 0 for a in actions}
                    q_table[state][action] += alpha * (reward + gamma * get_max_q(next_state) - q_table[state][action])
                    state = next_state
                else:
                    q_table[state][action] += alpha * (-5 - q_table[state][action])
        print(f"[Q-Learning] Trained Q-table: {q_table}")
        return q_table

def q_learning_step(q_table, current):
    if current not in q_table:
        print(f"[Q-Learning] No Q-table entry for state {current}")
        return current
    best_action = max(q_table[current], key=q_table[current].get)
    print(f"[Q-Learning] From {current}, next step: {best_action}")
    if isinstance(best_action, tuple):
        return (current[0] + best_action[0], current[1] + best_action[1])
    return best_action

def and_or_search_probabilistic(start, goal, graph, nodes=None):
    explored = set()
    path = []
    is_platform = isinstance(graph, dict) and nodes is not None
    def successors(state, action):
        results = []
        if is_platform:
            neighbors = graph.get(state, [])
            for neighbor_idx in neighbors:
                results.append((neighbor_idx, 0.7))
                other_neighbors = [n for n in neighbors if n != neighbor_idx]
                if other_neighbors:
                    random_neighbor = random.choice(other_neighbors)
                    results.append((random_neighbor, 0.3))
        else:
            x, y = state
            dx, dy = action
            intended = (x + dx, y + dy)
            side = (x + dy, y + dx)
            rows, cols = len(graph), len(graph[0])
            for (nx, ny), prob in [(intended, 0.7), (side, 0.3)]:
                if 0 <= nx < cols and 0 <= ny < rows and graph[ny][nx] == 0:
                    results.append(((nx, ny), prob))
        return results
    def search(state, current_path):
        if state == goal:
            path.append(state)
            return True
        if state in explored:
            return False
        explored.add(state)
        current_path.append(state)
        if is_platform:
            neighbors = graph.get(state, [])
        else:
            neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if not neighbors:
            return False
        for action in neighbors:
            outcomes = successors(state, action)
            if not outcomes:
                continue
            all_success = True
            for next_state, prob in outcomes:
                if next_state in current_path:
                    continue
                if not search(next_state, current_path.copy()):
                    all_success = False
                    break
            if all_success:
                path.append(state)
                return True
        current_path.pop()
        return False
    if search(start, []):
        path.reverse()
        print(f"[AND-OR] Found path: {path}")
    else:
        print(f"[AND-OR] No path found from {start} to {goal}")
    return path