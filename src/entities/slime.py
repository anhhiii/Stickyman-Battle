import pygame
import os
from src.ai.algorithms import bfs_path
from math import floor

class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, battle_base, name="slime"):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        if self.name == "slime1":
            self.follow_player = True
        self.alive = True
        self.speed = speed
        self.direction = -1  # -1: trái, 1: phải
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: Idle, 1: Jump, 2: Hurt, 3: Death
        self.update_time = pygame.time.get_ticks()
        self.health = 30  # Máu của slime
        self.battle_base = battle_base
        
        self.bfs_path = []  # đường đi kết quả từ BFS
        self.path_index = 0
        self.follow_player = False

        

        # Số khung hình cho từng trạng thái (dựa trên file thực tế)
        self.frame_counts = {
            'Idle': 7,
            'Jump': 6,  # Chỉ dùng Jump_Land cho simplicity
            'Hurt': 11,
            'Death': 14
        }

        # Định nghĩa các trạng thái hoạt hình
        self.animation_types = ['Idle', 'Jump', 'Hurt', 'Death']
        for animation in self.animation_types:
            temp_list = []
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            sprite_path = os.path.join(project_root, 'assets', 'sprites', 'slime', animation.lower())

            frame_count = self.frame_counts[animation]
            try:
                for i in range(frame_count):
                    img_path = os.path.join(sprite_path, f"{animation.capitalize()}_{i}.png")
                    if animation.lower() == 'jump':
                        img_path = os.path.join(sprite_path, f"Jump_Land_{i}.png")
                    if not os.path.exists(img_path):
                        print(f"Sprite file missing: {img_path}")
                        continue
                    img = pygame.image.load(img_path).convert_alpha()
                    # Scale khung hình
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)
                if not temp_list:
                    print(f"No valid sprites loaded for {animation}")
            except Exception as e:
                print(f"Error loading sprites for {animation}: {e}")
                temp_list.append(pygame.Surface((32, 32)))  # Placeholder 32x32
            self.animation_list.append(temp_list)

        if not self.animation_list or not self.animation_list[0]:
            print("Error: No sprites loaded for slime!")
            self.image = pygame.Surface((32, 32))
            self.image.fill((0, 255, 0))
        else:
            self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)  # Đảm bảo chân chạm đất
        print(f"Slime initialized at position: {self.rect.topleft}, size: {self.rect.width}x{self.rect.height}")

    def move (self):
        if self.follow_player and self.bfs_path:
            tx, ty = self.bfs_path[self.path_index]
            target_x = tx * self.battle_base.tile_width
            target_y = ty * self.battle_base.tile_height
            dx = dy = 0
            if self.rect.centerx < target_x:
                dx = self.speed
                self.direction = 1
                self.flip = False
            elif self.rect.centerx > target_x:
                dx = -self.speed
                self.direction = -1
                self.flip = True
            if self.rect.centery < target_y:
                dy = self.speed
            elif self.rect.centery > target_y:
                dy = -self.speed

            self.rect.x += dx
            self.check_collision('horizontal', dx)
            self.rect.y += dy
            self.check_collision('vertical', dy)

            # Nếu gần điểm tiếp theo thì chuyển sang điểm tiếp theo
            if abs(self.rect.centerx - target_x) < 5 and abs(self.rect.centery - target_y) < 5:
                self.path_index += 1
                if self.path_index >= len(self.bfs_path):
                    self.bfs_path = []
                    self.path_index = 0
            return  # không xử lý tiếp bên dưới nếu đang đi theo path
        dx = self.speed * self.direction
        dy = 0

        # Áp dụng trọng lực
        self.vel_y += 0.75
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        self.rect.x += dx
        self.check_collision('horizontal', dx)
        self.rect.y += dy
        self.check_collision('vertical', dy)

        # Đổi hướng khi chạm biên màn hình
        if self.rect.left < 200:
            self.rect.left = 200
            self.direction *= -1
            self.flip = not self.flip
        if self.rect.right > 600:
            self.rect.right = 600
            self.direction *= -1
            self.flip = not self.flip

        # Giới hạn trong màn hình
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600
            self.vel_y = 0
            self.in_air = False

        if not self.alive:
            return  # Dừng cập nhật di chuyển nếu slime đã chết


    def check_collision(self, direction, move_value):
        map_width = self.battle_base.map_width
        map_height = self.battle_base.map_height
        tile_width = self.battle_base.tile_width
        tile_height = self.battle_base.tile_height
        tile_layers = self.battle_base.tile_layers

        layer_idx = 1  # Layer "map"
        layer = tile_layers[layer_idx]

        start_col = max(0, (self.rect.left - tile_width) // tile_width)
        end_col = min(map_width, (self.rect.right + tile_width) // tile_width)
        start_row = max(0, (self.rect.top - tile_height) // tile_height)
        end_row = min(map_height, (self.rect.bottom + tile_height) // tile_height)

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                idx = row * map_width + col
                tile = layer[idx]
                if tile > 0:
                    tile_rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
                    if direction == 'horizontal':
                        if self.rect.colliderect(tile_rect):
                            if move_value > 0 and self.rect.right > tile_rect.left:
                                self.rect.right = tile_rect.left
                                self.direction *= -1
                                self.flip = not self.flip
                                # print(f"Slime collision (right) with tile at ({col * tile_width}, {row * tile_height})")
                            elif move_value < 0 and self.rect.left < tile_rect.right:
                                self.rect.left = tile_rect.right
                                self.direction *= -1
                                self.flip = not self.flip
                                # print(f"Slime collision (left) with tile at ({col * tile_width}, {row * tile_height})")
                    elif direction == 'vertical':
                        if self.rect.colliderect(tile_rect):
                            if move_value > 0 and self.rect.bottom > tile_rect.top:
                                self.rect.bottom = tile_rect.top
                                self.vel_y = 0
                                self.in_air = False
                                # print(f"Slime collision (bottom) with tile at ({col * tile_width}, {row * tile_height})")
                            elif move_value < 0 and self.rect.top < tile_rect.bottom:
                                self.rect.top = tile_rect.bottom
                                self.vel_y = 0
                                # print(f"Slime collision (top) with tile at ({col * tile_width}, {row * tile_height})")

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        bottomleft = self.rect.bottomleft
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = bottomleft

        if len(self.animation_list[self.action]) == 0:
            return

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

            if self.frame_index >= len(self.animation_list[self.action]):
                # Nếu đang Hurt thì quay lại Idle
                if self.action == 2:  # Hurt
                    self.update_action(0)  # Trở lại Idle
                elif self.action == 3:  # Death
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0
                if not self.alive:
                    return  # Không update animation nếu đã chết


        # print(f"Slime animation updated: action={self.action}, frame={self.frame_index}")

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            # print(f"Slime switching to action {self.action} with {len(self.animation_list[self.action])} frames")

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)  # Death

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        print(f"Slime drawn at: {self.rect.topleft}")