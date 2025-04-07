import pygame
from pygame.locals import *

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type="health"):
        super().__init__()
        
        # Chỉ có hai loại vật phẩm
        self.item_types = {
            "health": {"color": (0, 255, 0), "effect": "heal"},  # Hồi máu
            "coin": {"color": (255, 215, 0), "effect": "score"}   # Đồng xu
        }
        
        # Thiết lập thuộc tính
        if item_type not in self.item_types:
            raise ValueError(f"Invalid item_type. Must be 'health' or 'coin', got '{item_type}'")
        
        self.type = item_type
        self.image = pygame.Surface((20, 20))  # Kích thước vật phẩm
        self.image.fill(self.item_types[self.type]["color"])  # Màu theo loại
        self.rect = self.image.get_rect()
        self.rect.x = x  # Vị trí ban đầu
        self.rect.y = y
        
        # Hiệu ứng của vật phẩm
        self.effect = self.item_types[self.type]["effect"]
        self.value = 10  # Giá trị mặc định (10 HP hoặc 10 điểm)
        
    def apply_effect(self, player):
        """Áp dụng hiệu ứng của vật phẩm lên player"""
        if self.effect == "heal":
            # Giả sử player có thuộc tính health
            if hasattr(player, 'health'):
                player.health = min(player.health + self.value, 100)  # Giới hạn max 100
            print(f"Player healed by {self.value} HP")
        elif self.effect == "score":
            # Giả sử player có thuộc tính score
            if hasattr(player, 'score'):
                player.score += self.value
            print(f"Player gained {self.value} coins")
            
    def update(self):
        # Có thể thêm animation nếu muốn
        pass

# Cách sử dụng:
"""
items = pygame.sprite.Group()
health_item = Item(200, 480, "health")  # Vật phẩm máu
coin_item = Item(250, 480, "coin")      # Đồng xu
items.add(health_item, coin_item)
"""