from pathfinding import PlatformGrid, a_star_platform

class DecisionNode:
    """
    Một nút trong cây quyết định.
    """
    def __init__(self, condition=None, true_branch=None, false_branch=None, action=None):
        self.condition = condition  # Một hàm kiểm tra điều kiện (trả về True hoặc False)
        self.true_branch = true_branch  # Nhánh tiếp theo nếu điều kiện đúng
        self.false_branch = false_branch  # Nhánh tiếp theo nếu điều kiện sai
        self.action = action  # Hành động thực hiện nếu đây là nút lá

    def decide(self, context):
        """
        Duyệt qua cây quyết định dựa trên ngữ cảnh.
        """
        if self.action is not None:
            return self.action  # Nút lá, trả về hành động

        if self.condition(context):
            return self.true_branch.decide(context)  # Nếu điều kiện đúng, duyệt nhánh đúng
        else:
            return self.false_branch.decide(context)  # Nếu điều kiện sai, duyệt nhánh sai


# Điều kiện
def is_enemy_nearby(context):
    """
    Kiểm tra xem kẻ địch có ở gần không.
    """
    return abs(context['stickman']['x'] - context['enemy']['x']) < 100

def is_path_to_enemy_clear(context):
    """
    Kiểm tra xem có đường đi rõ ràng đến kẻ địch không (sử dụng thuật toán A*).
    """
    grid = context['grid']
    start = (context['stickman']['x'], context['stickman']['y'])
    end = (context['enemy']['x'], context['enemy']['y'])
    path = a_star_platform(grid, start, end)
    return len(path) > 0  # Trả về True nếu tồn tại đường đi


# Hành động
def attack():
    """
    Hành động: Tấn công kẻ địch.
    """
    return "attack"

def move_to_enemy(context):
    """
    Hành động: Di chuyển về phía kẻ địch (sử dụng thuật toán A*).
    """
    grid = context['grid']
    start = (context['stickman']['x'], context['stickman']['y'])
    end = (context['enemy']['x'], context['enemy']['y'])
    path = a_star_platform(grid, start, end)
    if path:
        next_step = path[1]  # Di chuyển đến bước tiếp theo trong đường đi
        return f"move_to ({next_step[0]}, {next_step[1]})"
    return "idle"

def idle():
    """
    Hành động: Đứng yên.
    """
    return "idle"


# Xây dựng cây quyết định
def build_decision_tree():
    """
    Xây dựng cây quyết định cho Stickman Battle.
    """
    # Nút lá
    attack_node = DecisionNode(action=attack)
    move_to_enemy_node = DecisionNode(action=move_to_enemy)
    idle_node = DecisionNode(action=idle)

    # Nút trung gian
    path_clear_node = DecisionNode(condition=is_path_to_enemy_clear, true_branch=move_to_enemy_node, false_branch=idle_node)
    root_node = DecisionNode(condition=is_enemy_nearby, true_branch=attack_node, false_branch=path_clear_node)

    return root_node



