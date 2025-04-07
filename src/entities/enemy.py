import pygame

class Enemy(pygame.sprite.Sprite):
    """
    Đại diện cho kẻ địch trong trò chơi.
    """
    def __init__(self, x, y, width=50, height=100, speed=2, health=100, color=(255, 0, 0)):
        """
        Khởi tạo kẻ địch.
        :param x: Tọa độ x ban đầu.
        :param y: Tọa độ y ban đầu.
        :param width: Chiều rộng của kẻ địch.
        :param height: Chiều cao của kẻ địch.
        :param speed: Tốc độ di chuyển.
        :param health: Máu của kẻ địch.
        :param color: Màu sắc của kẻ địch.
        """
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed
        self.health = health
        self.active = True  # Kẻ địch còn sống hay không
        self.direction = 1  # Hướng di chuyển (1: phải, -1: trái)

    def move(self, screen_width):
        """
        Di chuyển kẻ địch qua lại trong màn hình.
        :param screen_width: Chiều rộng màn hình.
        """
        if not self.active:
            return

        self.rect.x += self.direction * self.speed

        # Đổi hướng nếu chạm vào biên màn hình
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.direction *= -1

    def take_damage(self, damage):
        """
        Giảm máu của kẻ địch khi bị tấn công.
        :param damage: Lượng sát thương nhận được.
        """
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.active = False  # Kẻ địch chết

    def update(self, screen_width):
        """
        Cập nhật trạng thái của kẻ địch.
        :param screen_width: Chiều rộng màn hình.
        """
        if self.active:
            self.move(screen_width)