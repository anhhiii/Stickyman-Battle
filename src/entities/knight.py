import pygame
import os

class Knight(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, battle_base):
        super().__init__()
        self.rect = pygame.Rect(x, y, 49, 61)
        self.scale = scale
        self.speed = speed
        self.battle_base = battle_base
        self.flip = False
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
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
        self.attack_frame = 0
        self.jump_start_y = y

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

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = round(x / self.battle_base.tile_width) * self.battle_base.tile_width
        self.rect.y = round(y / self.battle_base.tile_height) * self.battle_base.tile_height
        self.adjust_to_ground()  # Căn chỉnh vị trí khởi tạo

    def adjust_to_ground(self):
        tile_width = self.battle_base.tile_width
        tile_height = self.battle_base.tile_height
        map_width = self.battle_base.map_width
        map_height = self.battle_base.map_height
        layer_ground = self.battle_base.tile_layers[1]
        valid_rows = [12, 18, 24, 30]

        col = self.rect.x // tile_width
        for row in reversed(valid_rows):
            idx = row * map_width + col
            if idx < len(layer_ground) and layer_ground[idx] >= 229:
                target_y = row * tile_height
                self.rect.bottom = target_y
                self.vel_y = 0
                self.in_air = False
                print(f"Đã căn chỉnh xuống ô đất tại y={target_y}")
                break
        else:
            self.in_air = True
            print("Không tìm thấy mặt đất, knight sẽ rơi")

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
        map_width_px = 800
        map_height_px = self.battle_base.map_height * self.battle_base.tile_height  # 38 * 16 = 608

        if self.rect.left < 0:
            self.rect.left = 0
            print("Chạm biên trái của bản đồ!")
        if self.rect.right > map_width_px:
            self.rect.right = map_width_px
            print("Chạm biên phải của bản đồ!")

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
            self.vel_y = -13
            self.jump = False
            self.in_air = True
            self.jump_start_y = self.rect.y

        self.vel_y += 0.75
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        prev_x = self.rect.x
        self.rect.x += dx
        self.rect.y += dy
        on_ground = self.check_collision('vertical', dy)

        # Kiểm tra va chạm trần (lòng đất) khi nhảy
        if self.vel_y < 0:  # Khi nhảy lên
            col_left = (self.rect.left) // self.battle_base.tile_width
            col_right = (self.rect.right - 1) // self.battle_base.tile_width
            map_width = self.battle_base.map_width
            layer_ground = self.battle_base.tile_layers[1]
            for col in range(col_left, col_right + 1):
                for row in [13, 19, 25]:  # Lòng đất
                    idx = row * map_width + col
                    if idx < len(layer_ground) and layer_ground[idx] >= 229:
                        tile_rect = pygame.Rect(col * self.battle_base.tile_width, row * self.battle_base.tile_height, self.battle_base.tile_width, self.battle_base.tile_height)
                        if self.rect.colliderect(tile_rect):
                            self.rect.top = tile_rect.bottom
                            self.vel_y = 0
                            print(f"Va chạm trần tại y={tile_rect.bottom}, knight y={self.rect.y}")
                            break
                    if self.vel_y == 0:
                        break
                if self.vel_y == 0:
                    break

        if not on_ground and prev_x // self.battle_base.tile_width != self.rect.x // self.battle_base.tile_width:
            self.in_air = True

        print(f"Knight pos: {self.rect.x}, {self.rect.y}, vel_y={self.vel_y}, rect.bottom={self.rect.bottom}")

        if self.rect.top > map_height_px or self.rect.bottom < 0:
            self.in_air = True
            print(f"Knight rơi ra khỏi màn hình tại y={self.rect.y}")

    def check_collision(self, direction, value):
        map_width = self.battle_base.map_width
        map_height = self.battle_base.map_height
        tile_width = self.battle_base.tile_width
        tile_height = self.battle_base.tile_height
        layer_ground = self.battle_base.tile_layers[1]
        on_ground = False

        valid_rows = [12, 18, 24, 30]  # Chỉ mặt đất, không cần lòng đất vì không đứng trên đó

        if direction == 'vertical':
            col_left = (self.rect.left) // tile_width
            col_right = (self.rect.right - 1) // tile_width
            for col in range(col_left, col_right + 1):
                for row in reversed(valid_rows):  # Kiểm tra từ dưới lên
                    idx = row * map_width + col
                    if idx < len(layer_ground) and layer_ground[idx] >= 229:
                        tile_rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
                        if self.rect.colliderect(tile_rect):
                            print(f"Va chạm với ô {layer_ground[idx]} tại ({col}, {row}), tile_rect={tile_rect}")
                            if value > 0:  # Rơi xuống
                                self.rect.bottom = tile_rect.top
                                self.vel_y = 0
                                self.in_air = False
                                on_ground = True
                                print(f"Đáp xuống ô tại y={tile_rect.top}, knight y={self.rect.y}")
                            break
                    if on_ground:
                        break
                if on_ground:
                    break

            if value > 0 and not on_ground:
                self.in_air = True
                print(f"Không va chạm, knight rơi tại y={self.rect.y}")

        return on_ground
    
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