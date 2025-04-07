import pygame

class Projectile(pygame.sprite.Sprite):
    """
    Đại diện cho một vật thể bay (đạn, tên, kỹ năng) trong trò chơi.
    """
    def __init__(self, x, y, direction, speed=10, damage=20, width=10, height=5, color=(255, 255, 0)):
        """
        Khởi tạo vật thể bay.
        :param x: Tọa độ x ban đầu.
        :param y: Tọa độ y ban đầu.
        :param direction: Hướng di chuyển (-1: trái, 1: phải).
        :param speed: Tốc độ di chuyển.
        :param damage: Sát thương gây ra.
        :param width: Chiều rộng của vật thể bay.
        :param height: Chiều cao của vật thể bay.
        :param color: Màu sắc của vật thể bay.
        """
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.active = True  # Vật thể bay còn tồn tại hay không

    def update(self, screen_width):
        """
        Cập nhật vị trí của vật thể bay.
        :param screen_width: Chiều rộng màn hình, dùng để kiểm tra vật thể bay có ra khỏi màn hình không.
        """
        if not self.active:
            return

        # Di chuyển vật thể bay
        self.rect.x += self.direction * self.speed

        # Kiểm tra nếu vật thể bay ra khỏi màn hình
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.active = False

    def collide(self, target):
        """
        Xử lý va chạm với mục tiêu.
        :param target: Đối tượng bị va chạm (ví dụ: Enemy hoặc Player).
        """
        if self.active and self.rect.colliderect(target.rect):
            target.take_damage(self.damage)  # Gây sát thương cho mục tiêu
            self.active = False  # Vật thể bay biến mất sau khi va chạm