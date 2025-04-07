import heapq
import math
from typing import Dict, List, Tuple, Set

class Node:
    def __init__(self, x, y, walkable=True):
        self.x = x
        self.y = y
        self.walkable = walkable  # True nếu có thể đi qua, False nếu là chướng ngại vật
        self.platform = False     # True nếu là bề mặt platform mà entity có thể đứng lên
        self.parent = None
        self.g = 0  # Chi phí từ điểm bắt đầu đến node này
        self.h = 0  # Heuristic (ước lượng) từ node này đến đích
        self.f = 0  # f = g + h
        self.jump_parent = False  # Đánh dấu nếu cần phải nhảy để đến node này

    def __lt__(self, other):
        return self.f < other.f
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

class PlatformGrid:
    def __init__(self, width, height, platform_data):
        """
        Khởi tạo grid với dữ liệu platform
        
        Parameters:
            width: Chiều rộng của grid
            height: Chiều cao của grid
            platform_data: List các tuple (x1, y1, x2, y2) biểu diễn các platform
                           hoặc ma trận 2D với 1 là platform, 0 là không có gì
        """
        self.width = width
        self.height = height
        self.nodes = [[Node(x, y) for y in range(height)] for x in range(width)]
        
        # Khởi tạo platform từ dữ liệu
        self._initialize_platforms(platform_data)
        
        # Thông số của quái vật
        self.jump_height = 3  # Độ cao tối đa quái vật có thể nhảy
        self.max_fall = 10    # Độ cao tối đa quái vật có thể rơi an toàn
    
    def _initialize_platforms(self, platform_data):
        """Khởi tạo các platform trong grid"""
        if isinstance(platform_data, list) and isinstance(platform_data[0], tuple):
            # Dữ liệu dạng list các tuple (x1, y1, x2, y2)
            for x1, y1, x2, y2 in platform_data:
                for x in range(x1, x2 + 1):
                    for y in range(y1, y2 + 1):
                        if 0 <= x < self.width and 0 <= y < self.height:
                            self.nodes[x][y].walkable = False  # Không thể đi xuyên qua platform
                            # Đánh dấu phần trên cùng của platform là có thể đứng lên
                            if y == y1:
                                self.nodes[x][y1-1].platform = True
        else:
            # Dữ liệu dạng ma trận 2D
            for x in range(self.width):
                for y in range(self.height):
                    if platform_data[y][x] == 1:  # Giả sử 1 là platform
                        self.nodes[x][y].walkable = False
                        # Đánh dấu phần trên cùng của platform là có thể đứng lên
                        if y > 0:
                            self.nodes[x][y-1].platform = True
    
    def is_valid_position(self, x, y):
        """Kiểm tra xem vị trí (x, y) có hợp lệ không"""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_standing_position(self, x, y):
        """Kiểm tra xem có thể đứng tại vị trí (x, y) không"""
        # Phải ở trên một platform hoặc trên mặt đất
        if not self.is_valid_position(x, y):
            return False
        
        if y + 1 >= self.height:
            return True  # Đang ở trên mặt đất (đáy map)
        
        return self.nodes[x][y].walkable and self.nodes[x][y].platform
    
    def can_jump_to(self, current_x, current_y, target_x, target_y):
        """Kiểm tra xem quái vật có thể nhảy từ (current_x, current_y) đến (target_x, target_y) không"""
        # Kiểm tra khoảng cách nhảy ngang
        horizontal_dist = abs(target_x - current_x)
        
        # Kiểm tra độ cao nhảy lên
        if target_y < current_y:  # Nhảy lên
            vertical_dist = current_y - target_y
            return vertical_dist <= self.jump_height and horizontal_dist <= self.jump_height
        else:  # Nhảy/rơi xuống
            vertical_dist = target_y - current_y
            return vertical_dist <= self.max_fall and horizontal_dist <= self.jump_height
    
    def get_neighbors(self, node):
        """Lấy các node kề có thể di chuyển đến từ node hiện tại"""
        neighbors = []
        x, y = node.x, node.y
        
        # Di chuyển sang trái/phải (nếu đang ở trên platform hoặc mặt đất)
        if self.is_standing_position(x, y):
            # Di chuyển sang trái
            if self.is_valid_position(x - 1, y) and self.nodes[x - 1][y].walkable:
                neighbors.append((self.nodes[x - 1, y], False))
            
            # Di chuyển sang phải
            if self.is_valid_position(x + 1, y) and self.nodes[x + 1][y].walkable:
                neighbors.append((self.nodes[x + 1, y], False))
        
        # Kiểm tra khả năng nhảy lên các platform khác
        for jump_x in range(max(0, x - self.jump_height), min(self.width, x + self.jump_height + 1)):
            for jump_y in range(max(0, y - self.jump_height), min(self.height, y + self.max_fall + 1)):
                if (jump_x != x or jump_y != y) and self.is_standing_position(jump_x, jump_y):
                    if self.can_jump_to(x, y, jump_x, jump_y):
                        # Đảm bảo đường đi không bị chặn bởi platform
                        if self._check_jump_path_clear(x, y, jump_x, jump_y):
                            neighbors.append((self.nodes[jump_x][jump_y], True))
        
        return neighbors
    
    def _check_jump_path_clear(self, x1, y1, x2, y2):
        """Kiểm tra xem đường nhảy từ (x1, y1) đến (x2, y2) có bị chặn bởi platform không"""
        # Thuật toán Bresenham để kiểm tra đường đi
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        while x1 != x2 or y1 != y2:
            if not self.is_valid_position(x1, y1) or not self.nodes[x1][y1].walkable:
                return False
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
        
        return True
    
    def get_node(self, x, y):
        """Lấy node tại vị trí (x, y)"""
        if self.is_valid_position(x, y):
            return self.nodes[x][y]
        return None

def heuristic(a, b):
    """Hàm ước lượng khoảng cách từ node a đến node b"""
    # Khoảng cách Euclidean
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

def a_star_platform(grid, start, end):
    """
    Thuật toán A* cho game platform 2D
    
    Parameters:
        grid: PlatformGrid object
        start: tuple (x, y) điểm bắt đầu
        end: tuple (x, y) điểm kết thúc
        
    Returns:
        List các điểm [(x, y, jump)] với jump=True nếu cần nhảy
    """
    start_node = grid.get_node(start[0], start[1])
    end_node = grid.get_node(end[0], end[1])
    
    if not start_node or not end_node:
        return []
    
    open_set = []
    closed_set = set()
    
    start_node.g = 0
    start_node.h = heuristic(start_node, end_node)
    start_node.f = start_node.h
    
    heapq.heappush(open_set, start_node)
    
    while open_set:
        current = heapq.heappop(open_set)
        
        if current == end_node:
            # Tạo đường đi
            path = []
            while current:
                jump = getattr(current, 'jump_parent', False)
                path.append((current.x, current.y, jump))
                current = current.parent
            return path[::-1]
        
        closed_set.add(current)
        
        for neighbor, jump_required in grid.get_neighbors(current):
            if neighbor in closed_set:
                continue
            
            # Chi phí di chuyển (cao hơn nếu cần nhảy)
            move_cost = 1.5 if jump_required else 1
            tentative_g = current.g + move_cost
            
            is_better = False
            if neighbor not in open_set:
                neighbor.h = heuristic(neighbor, end_node)
                is_better = True
                heapq.heappush(open_set, neighbor)
            elif tentative_g < neighbor.g:
                is_better = True
            
            if is_better:
                neighbor.parent = current
                neighbor.jump_parent = jump_required
                neighbor.g = tentative_g
                neighbor.f = neighbor.g + neighbor.h
    
    return []