import pygame
from src.entities.projectile import Projectile

class Weapon:
    """
    Đại diện cho vũ khí trong trò chơi.
    """
    def __init__(self, owner, cooldown=500, projectile_speed=15, projectile_damage=25, projectile_color=(255, 255, 0)):
        """
        Khởi tạo vũ khí.
        :param owner: Chủ sở hữu của vũ khí (ví dụ: Player hoặc Enemy).
        :param cooldown: Thời gian hồi chiêu giữa các lần bắn (ms).
        :param projectile_speed: Tốc độ của đạn bắn ra.
        :param projectile_damage: Sát thương của đạn.
        :param projectile_color: Màu sắc của đạn.
        """
        self.owner = owner
        self.cooldown = cooldown
        self.last_shot_time = 0
        self.projectile_speed = projectile_speed
        self.projectile_damage = projectile_damage
        self.projectile_color = projectile_color

    def shoot(self, projectiles_group, current_time):
        """
        Bắn đạn nếu vũ khí không trong thời gian hồi chiêu.
        :param projectiles_group: Nhóm chứa các vật thể bay (đạn).
        :param current_time: Thời gian hiện tại (pygame.time.get_ticks()).
        """
        # Kiểm tra nếu vũ khí đang trong thời gian hồi chiêu
        if current_time - self.last_shot_time < self.cooldown:
            return

        # Kiểm tra nếu chủ sở hữu có thuộc tính 'rect' và 'direction'
        if not hasattr(self.owner, 'rect') or not hasattr(self.owner, 'direction'):
            raise AttributeError("Owner must have 'rect' and 'direction' attributes.")

        # Lấy vị trí và hướng của chủ sở hữu
        x = self.owner.rect.centerx
        y = self.owner.rect.centery
        direction = self.owner.direction

        # Kiểm tra hướng hợp lệ (-1 hoặc 1)
        if direction not in [-1, 1]:
            raise ValueError("Direction must be -1 (left) or 1 (right).")

        # Tạo đạn mới
        projectile = Projectile(
            x=x,
            y=y,
            direction=direction,
            speed=self.projectile_speed,
            damage=self.projectile_damage,
            color=self.projectile_color
        )

        # Thêm đạn vào nhóm
        projectiles_group.add(projectile)

        # Cập nhật thời gian bắn cuối cùng
        self.last_shot_time = current_time