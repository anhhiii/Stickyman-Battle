import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 64))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 5
        self.jump_power = -15
        self.velocity_y = 0
        self.gravity = 0.8
        
        self.is_jumping = False
        self.on_ground = True
        
        self.attack_cooldown = 0
        self.attack_duration = 20
        
        self.inventory = []
        self.health = 100  # Thêm máu ban đầu
        self.score = 0     # Thêm điểm số ban đầu
        
    # Các hàm khác giữ nguyên, chỉ cập nhật pickup_item
    def pickup_item(self, item):
        self.inventory.append(item)
        item.apply_effect(self)  # Áp dụng hiệu ứng lên player
        print(f"Picked up {item.type}")
        
    def update(self, item_group):
        # Xử lý gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        
        # Kiểm tra va chạm với mặt đất (giả sử y=500 là mặt đất)
        if self.rect.bottom > 500:
            self.rect.bottom = 500
            self.velocity_y = 0
            self.on_ground = True
            self.is_jumping = False
            
        # Giảm cooldown tấn công
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # Kiểm tra va chạm với vật phẩm
        self.check_item_collision(item_group)
            
    def handle_input(self, keys):
        # Di chuyển trái phải
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed
            
        # Nhảy
        if keys[K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.is_jumping = True
            self.on_ground = False
            
        # Tấn công cơ bản
        if keys[K_j] and self.attack_cooldown == 0:
            self.basic_attack()
            
        # Chiêu thức đặc biệt
        if keys[K_k] and self.attack_cooldown == 0:
            self.special_attack()
            
    def basic_attack(self):
        self.attack_cooldown = 20
        print("Basic Attack!")
        
    def special_attack(self):
        self.attack_cooldown = 30
        print("Special Attack!")
        
    def check_item_collision(self, item_group):
        # Kiểm tra va chạm với các vật phẩm
        collided_items = pygame.sprite.spritecollide(self, item_group, True)  # True để xóa item khi nhặt
        for item in collided_items:
            self.pickup_item(item)
            
    def pickup_item(self, item):
        # Xử lý khi nhặt vật phẩm
        self.inventory.append(item)
        print(f"Picked up {item.__class__.__name__}")  # In thông báo tạm thời
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)