import pygame

class Player:
    """
    Đại diện cho nhân vật người chơi trong trò chơi Stickman Battle.
    """
    def __init__(self, x, y, width=50, height=100, speed=5, health=100):
        """
        Khởi tạo nhân vật người chơi.
        :param x: Tọa độ x ban đầu.
        :param y: Tọa độ y ban đầu.
        :param width: Chiều rộng của nhân vật.
        :param height: Chiều cao của nhân vật.
        :param speed: Tốc độ di chuyển của nhân vật.
        :param health: Máu của nhân vật.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health
        self.is_jumping = False
        self.jump_speed = 10
        self.gravity = 1
        self.vertical_velocity = 0
        self.on_ground = True
        self.active = True  # Nhân vật còn sống hay không

    def move(self, keys, screen_width):
        """
        Di chuyển nhân vật dựa trên đầu vào từ bàn phím.
        :param keys: Các phím đang được nhấn.
        :param screen_width: Chiều rộng của màn hình.
        """
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            if self.x < 0:
                self.x = 0  # Không cho phép di chuyển ra ngoài màn hình bên trái
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            if self.x + self.width > screen_width:
                self.x = screen_width - self.width  # Không cho phép di chuyển ra ngoài màn hình bên phải

    def jump(self):
        """
        Xử lý hành động nhảy của nhân vật.
        """
        if self.on_ground:
            self.is_jumping = True
            self.vertical_velocity = -self.jump_speed
            self.on_ground = False

    def apply_gravity(self, ground_level):
        """
        Áp dụng trọng lực để xử lý rơi tự do và nhảy.
        :param ground_level: Mức đất (y) mà nhân vật không thể rơi xuống dưới.
        """
        if not self.on_ground:
            self.vertical_velocity += self.gravity
            self.y += self.vertical_velocity

            if self.y >= ground_level:
                self.y = ground_level
                self.on_ground = True
                self.is_jumping = False

    def attack(self):
        """
        Hành động tấn công.
        """
        print("Player is attacking!")

    def take_damage(self, damage):
        """
        Giảm máu của nhân vật khi bị tấn công.
        :param damage: Lượng sát thương nhận được.
        """
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.active = False  # Nhân vật chết

    def is_alive(self):
        """
        Kiểm tra xem nhân vật còn sống hay không.
        :return: True nếu còn sống, False nếu đã chết.
        """
        return self.active