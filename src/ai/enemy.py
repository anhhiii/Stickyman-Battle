from decision_tree import build_decision_tree
from pathfinding import PlatformGrid, a_star_platform

class Enemy:
    """
    Đại diện cho kẻ địch trong trò chơi Stickman Battle.
    """
    def __init__(self, x, y, width=50, height=100, speed=3, health=100):
        """
        Khởi tạo kẻ địch.
        :param x: Tọa độ x ban đầu.
        :param y: Tọa độ y ban đầu.
        :param width: Chiều rộng của kẻ địch.
        :param height: Chiều cao của kẻ địch.
        :param speed: Tốc độ di chuyển của kẻ địch.
        :param health: Máu của kẻ địch.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health
        self.decision_tree = build_decision_tree()  # Cây quyết định cho hành vi của kẻ địch
        self.active = True  # Kẻ địch còn sống hay không

    def move(self, grid, target_x, target_y):
        """
        Di chuyển kẻ địch về phía mục tiêu (Stickman) bằng thuật toán A*.
        :param grid: Lưới nền tảng (PlatformGrid).
        :param target_x: Tọa độ x của mục tiêu.
        :param target_y: Tọa độ y của mục tiêu.
        """
        if not self.active:
            return

        start = (self.x, self.y)
        end = (target_x, target_y)
        path = a_star_platform(grid, start, end)

        if len(path) > 1:
            next_step = path[1]  # Lấy bước tiếp theo trong đường đi
            self.x, self.y = next_step

    def take_damage(self, damage):
        """
        Giảm máu của kẻ địch khi bị tấn công.
        :param damage: Lượng sát thương nhận được.
        """
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.active = False  # Kẻ địch chết

    def decide_action(self, context):
        """
        Quyết định hành động dựa trên cây quyết định và ngữ cảnh.
        :param context: Ngữ cảnh hiện tại (bao gồm vị trí Stickman, Enemy, và lưới).
        :return: Hành động được chọn.
        """
        if not self.active:
            return "idle"  # Kẻ địch không làm gì nếu đã chết

        action = self.decision_tree.decide(context)
        return action(context) if callable(action) else action

    