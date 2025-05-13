from collections import deque

def bfs_path(start, goal, map_data, map_width, map_height):
    queue = deque()
    visited = set()
    parent = {}

    queue.append(start)
    visited.add(start)

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Left, Right, Up, Down

    while queue:
        current = queue.popleft()

        if current == goal:
            # Truy vết đường đi từ goal về start
            path = []
            while current != start:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path

        for dx, dy in directions:
            nx = current[0] + dx
            ny = current[1] + dy
            neighbor = (nx, ny)

            if (0 <= nx < map_width and 0 <= ny < map_height and
                neighbor not in visited and
                map_data[ny * map_width + nx] > 0):  # Tile không phải trống
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    return []  # Không tìm được đường
