import pygame
import os

class Knight(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, battle_base):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.direction = 1  # 1: phải, -1: trái
        self.vel_y = 0
        self.jump = False
        self.in_air = True  # Mặc định là True để knight rơi khi khởi động
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: Idle, 1: Walk, 2: Jump, 3: Death, 4: Attack, 5: Block, 6: Cast, 7: Crouch, 8: Dash, 9: Dizzy, 10: Hurt, 11: JumpAttack, 12: Strike, 13: Win
        self.update_time = pygame.time.get_ticks()
        self.health = 100
        self.attack = False
        self.block = False
        self.cast = False
        self.crouch = False
        self.dash = False
        self.battle_base = battle_base  # Tham chiếu đến BattleBase để lấy thông tin va chạm

        # Định nghĩa các trạng thái hoạt hình
        self.animation_types = ['Idle', 'Walk', 'Jump', 'Death', 'Attack', 'Block', 'Cast', 'Crouch', 'Dash', 'Dizzy', 'Hurt', 'JumpAttack', 'Strike', 'Win']
        for animation in self.animation_types:
            temp_list = []
            sprite_path = os.path.join('assets', 'sprites', 'knight files', 'knight png', animation)
            try:
                num_of_frames = len(os.listdir(sprite_path))
                print(f"Loading {animation} with {num_of_frames} frames from {sprite_path}")
                for i in range(num_of_frames):
                    img_path = os.path.join(sprite_path, f'{i}.png')
                    if not os.path.exists(img_path):
                        print(f"Sprite file missing: {img_path}")
                        continue
                    img = pygame.image.load(img_path).convert_alpha()
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)
            except Exception as e:
                print(f"Error loading sprites for {animation}: {e}")
                temp_list.append(pygame.Surface((50, 50)))
            self.animation_list.append(temp_list)

        if not self.animation_list or not self.animation_list[0]:
            print("Error: No sprites loaded for knight!")
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
        else:
            self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)  # Sử dụng bottomleft để đặt chân knight trên sàn
        print(f"Knight initialized at position: {self.rect.topleft}, size: {self.rect.width}x{self.rect.height}")

    def load_sprite(self, animation):
        idx = self.animation_types.index(animation)
        print(f"Manually loading sprite for {animation}, frame count: {len(self.animation_list[idx])}")
        if self.animation_list[idx]:
            self.image = self.animation_list[idx][self.frame_index]

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.jump and not self.in_air:
            self.vel_y = -15  # Tăng lực nhảy
            self.jump = False
            self.in_air = True

        self.vel_y += 0.75  # GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        self.rect.x += dx
        self.check_collision('horizontal', dx)
        self.rect.y += dy
        self.check_collision('vertical', dy)

        # Giới hạn trong màn hình
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600
            self.vel_y = 0
            self.in_air = False

    def check_collision(self, direction, move_value):
        map_width = self.battle_base.map_width
        map_height = self.battle_base.map_height
        tile_width = self.battle_base.tile_width
        tile_height = self.battle_base.tile_height
        tile_layers = self.battle_base.tile_layers

        layer_idx = 1  # Layer "map"
        layer = tile_layers[layer_idx]

        # Chỉ kiểm tra tile gần chân knight
        start_col = max(0, (self.rect.left - tile_width) // tile_width)
        end_col = min(map_width, (self.rect.right + tile_width) // tile_width)
        start_row = max(0, (self.rect.bottom - self.rect.height + 10) // tile_height)  # Bắt đầu từ gần chân với buffer
        end_row = min(map_height, (self.rect.bottom + tile_height) // tile_height)

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                idx = row * map_width + col
                tile = layer[idx]
                if tile > 0:
                    tile_rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
                    collision_buffer = 2
                    if direction == 'horizontal':
                        if self.rect.colliderect(tile_rect):
                            if move_value > 0 and self.rect.right > tile_rect.left and self.rect.right <= tile_rect.left + collision_buffer:
                                self.rect.right = tile_rect.left
                                print(f"Collision (right) with tile at ({col * tile_width}, {row * tile_height})")
                            elif move_value < 0 and self.rect.left < tile_rect.right and self.rect.left >= tile_rect.right - collision_buffer:
                                self.rect.left = tile_rect.right
                                print(f"Collision (left) with tile at ({col * tile_width}, {row * tile_height})")
                    elif direction == 'vertical':
                        if self.rect.colliderect(tile_rect):
                            if move_value > 0 and self.rect.bottom > tile_rect.top and self.rect.bottom <= tile_rect.top + collision_buffer:
                                self.rect.bottom = tile_rect.top
                                self.vel_y = 0
                                self.in_air = False
                                print(f"Collision (bottom) with tile at ({col * tile_width}, {row * tile_height})")
                            elif move_value < 0 and self.rect.top < tile_rect.bottom and self.rect.top >= tile_rect.bottom - collision_buffer:
                                self.rect.top = tile_rect.bottom
                                self.vel_y = 0
                                print(f"Collision (top) with tile at ({col * tile_width}, {row * tile_height})")

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        if len(self.animation_list[self.action]) == 0:
            print(f"No frames for action {self.action}")
            return
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action in [3, 9, 10, 13]:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            print(f"Switching to action {self.action} with {len(self.animation_list[self.action])} frames")

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)  # Death

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)