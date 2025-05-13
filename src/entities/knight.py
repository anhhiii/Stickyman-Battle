import pygame
import os

class Knight(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, battle_base):
        super().__init__()
        self.rect = pygame.Rect(x, y, 49, 61)  # Kích thước của Knight
        self.scale = scale
        self.speed = speed
        self.battle_base = battle_base
        self.flip = False
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = False
        self.attack = False
        self.block = False
        self.cast = False
        self.crouch = False
        self.dash = False
        self.alive = True
        self.health = 100
        self.action = 0
        self.frame_index = 0
        self.animation_types = ['Idle', 'Walk', 'Jump', 'Attack', 'Block', 'Cast', 'Crouch', 'Dash', 'Dizzy', 'Hurt', 'JumpAttack']
        self.animation_list = []
        self.update_time = pygame.time.get_ticks()
        self.attack_frame = 0  # Thêm biến để đếm frame của Attack
        self.jump_start_y = y  # Lưu vị trí y ban đầu
        
        # Tải sprite ban đầu cho tất cả hành động
        for action in self.animation_types:
            sprite_list = []
            action_folder = os.path.join('assets', 'sprites', 'knight files', 'knight png', action)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            sprite_path = os.path.join(project_root, action_folder)
            for file in os.listdir(sprite_path):
                if file.endswith('.png'):
                    img_path = os.path.join(sprite_path, file)
                    img = pygame.image.load(img_path).convert_alpha()
                    img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
                    sprite_list.append(img)
            self.animation_list.append(sprite_list)

        if not self.animation_list or not self.animation_list[0]:
            raise ValueError("Failed to load any sprites for Knight!")

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = round(x / self.battle_base.tile_width) * self.battle_base.tile_width
        self.rect.y = round(y / self.battle_base.tile_height) * self.battle_base.tile_height

    def load_sprite(self, action):
        action_folder = action
        sprite_list = []
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        sprite_path = os.path.join(project_root, 'assets', 'sprites', 'knight', action_folder)

        for file in os.listdir(sprite_path):
            if file.endswith('.png'):
                img_path = os.path.join(sprite_path, file)
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
                sprite_list.append(img)

        action_index = self.animation_types.index(action)
        self.animation_list[action_index] = sprite_list
        self.frame_index = 0

    def move(self, left, right):
        map_width_px = self.battle_base.map_width * self.battle_base.tile_width
        map_height_px = self.battle_base.map_height * self.battle_base.tile_height
        print(f"Map bounds: width={map_width_px}px, height={map_height_px}px")

        if self.rect.left < 0:
            self.rect.left = 0
            print("Hit left boundary!")
        if self.rect.right > map_width_px:
            self.rect.right = map_width_px
            print("Hit right boundary!")
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0
            print("Hit top boundary!")
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
            print(f"Moving left: flip={self.flip}, direction={self.direction}")
        if right:
            dx = self.speed
            self.flip = False
            self.direction = 1
            print(f"Moving right: flip={self.flip}, direction={self.direction}")
        if self.jump and not self.in_air:
            print("Knight jumps!")
            self.vel_y = -13
            self.jump = False
            self.in_air = True
            self.jump_start_y = self.rect.y

        self.vel_y += 0.75
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        if self.in_air and self.vel_y < 0:
            height_jumped = self.jump_start_y - self.rect.y
            if height_jumped >= 112:
                self.rect.y = self.jump_start_y - 112
                self.vel_y = 0
                print(f"Reached max jump height: {height_jumped} pixels")

        self.in_air = True

        self.rect.x += dx
        # self.check_collision('horizontal', dx)
        self.rect.y += dy
        # self.check_collision('vertical', dy)
        print(f"Knight pos: {self.rect.x}, {self.rect.y}, vel_y={self.vel_y}")

    def check_collision(self, direction, value):
        map_width = self.battle_base.map_width
        map_height = self.battle_base.map_height
        tile_width = self.battle_base.tile_width
        tile_height = self.battle_base.tile_height

        layer_ground = self.battle_base.tile_layers[1]
        on_ground = False

        for row in range(map_height):
            for col in range(map_width):
                idx = row * map_width + col
                tile = layer_ground[idx]
                if tile >= 229:
                    tile_rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
                    if self.rect.colliderect(tile_rect):
                        if direction == 'horizontal':
                            if value > 0:
                                self.rect.right = tile_rect.left
                                print(f"Collision right at tile {tile} at ({col}, {row})")
                            elif value < 0:
                                self.rect.left = tile_rect.right
                                print(f"Collision left at tile {tile} at ({col}, {row})")
                        elif direction == 'vertical':
                            if value > 0:
                                self.rect.bottom = tile_rect.top
                                self.vel_y = 0
                                self.in_air = False
                                on_ground = True
                                print(f"Landing on tile {tile} at ({col}, {row})")
                            elif value < 0:
                                self.rect.top = tile_rect.bottom
                                self.vel_y = 0
                                print(f"Hitting ceiling at tile {tile} at ({col}, {row})")

        if direction == 'vertical' and value > 0 and not on_ground:
            self.in_air = True
            print(f"No collision, Knight is falling at {self.rect.x}, {self.rect.y}")

    def update_animation(self):
        cooldown = 100
        if self.action < 0 or self.action >= len(self.animation_list):
            print(f"Error: Invalid action index {self.action}, resetting to Idle (0)")
            self.action = 0

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            print(f"Resetting frame index to 0 for action {self.action}")
            if self.action == 3:  # Nếu là Attack (index 3)
                self.attack = False  # Tắt trạng thái attack khi animation kết thúc
                self.attack_frame = 0  # Reset frame đếm

        self.image = self.animation_list[self.action][self.frame_index]
        print(f"Animation: action={self.action}, frame={self.frame_index}")
        if pygame.time.get_ticks() - self.update_time > cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.action == 3:  # Nếu đang trong trạng thái Attack
                self.attack_frame += 1
                print(f"Attack frame: {self.attack_frame}")
            print(f"Updating frame to {self.frame_index}")

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            print(f"Updated action to {new_action}")
            if new_action == 3:  # Nếu chuyển sang Attack
                self.attack = True
                self.attack_frame = 0  # Bắt đầu đếm frame cho Attack

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)  # Death

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)