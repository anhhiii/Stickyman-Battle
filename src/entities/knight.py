import pygame
import os

class Knight(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, battle_base):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True  # Khởi tạo Knight trên không để nó rơi xuống
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.attack = False
        self.block = False
        self.cast = False
        self.crouch = False
        self.dash = False
        self.update_time = pygame.time.get_ticks()
        self.health = 100
        self.battle_base = battle_base

        self.animation_types = ['Idle', 'Walk', 'Jump', 'Attack']
        for animation in self.animation_types:
            temp_list = []
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            sprite_path = os.path.join(project_root, 'assets', 'sprites', 'knight files', 'knight png', animation)
            for i in range(6 if animation != 'Jump' else 2):
                img_path = os.path.join(sprite_path, f"{i}.png")
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        # Căn chỉnh vị trí với lưới bản đồ (mỗi ô 16x16 pixel)
        self.rect.x = round(x / self.battle_base.tile_width) * self.battle_base.tile_width
        self.rect.y = round(y / self.battle_base.tile_height) * self.battle_base.tile_height

    def move(self, left, right):
        map_width_px = self.battle_base.map_width * self.battle_base.tile_width
        map_height_px = self.battle_base.map_height * self.battle_base.tile_height

        # Giới hạn Knight không ra khỏi bản đồ thật
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > map_width_px:
            self.rect.right = map_width_px
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > map_height_px:
            self.rect.bottom = map_height_px
            self.vel_y = 0
            self.in_air = False

        dx = 0
        dy = 0
        if left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if self.jump and not self.in_air:
            print("Knight jumps!")
            self.vel_y = -30
            self.jump = False
            self.in_air = True

        # Áp dụng trọng lực
        self.vel_y += 0.75
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Đặt in_air = True trước khi kiểm tra va chạm
        self.in_air = True  # Đặt lại để đảm bảo Knight luôn rơi cho đến khi va chạm

        self.rect.x += dx
        self.check_collision('horizontal', dx)
        self.rect.y += dy
        self.check_collision('vertical', dy)
        print(f"Knight pos: {self.rect.x}, {self.rect.y}")

    def check_collision(self, direction, value):
        map_width = self.battle_base.map_width
        map_height = self.battle_base.map_height
        tile_width = self.battle_base.tile_width
        tile_height = self.battle_base.tile_height

        # Kiểm tra layer "ground" (index 1) - Nền tảng Knight có thể đứng
        layer_ground = self.battle_base.tile_layers[1]
        for row in range(map_height):
            for col in range(map_width):
                idx = row * map_width + col
                tile = layer_ground[idx]
                if tile >= 229:  # Nền tảng Knight có thể đứng
                    tile_rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
                    if self.rect.colliderect(tile_rect):
                        if direction == 'vertical':
                            if value > 0:  # Rơi xuống
                                self.rect.bottom = tile_rect.top
                                self.vel_y = 0
                                self.in_air = False
                                print(f"Landing on tile {tile} at ({col}, {row})")
                            elif value < 0:  # Nhảy lên
                                self.rect.top = tile_rect.bottom
                                self.vel_y = 0
                                print(f"Hitting ceiling at tile {tile} at ({col}, {row})")
        # Nếu không va chạm, đảm bảo Knight vẫn ở trạng thái rơi
        if direction == 'vertical' and value > 0 and self.in_air:
            print(f"No collision, Knight is falling at {self.rect.x}, {self.rect.y}")

    def update_animation(self):
        cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)  # Death

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)