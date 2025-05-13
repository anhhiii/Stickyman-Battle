import pygame
import os

class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, battle_base, move_area=None):
        pygame.sprite.Sprite.__init__(self)
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
        self.health = 30
        self.battle_base = battle_base
        self.move_area = move_area

        self.frame_counts = {
            'Idle': 7,
            'Jump': 6,
            'Hurt': 11,
            'Death': 14
        }

        self.animation_types = ['Idle', 'Jump', 'Hurt', 'Death']
        for animation in self.animation_types:
            temp_list = []
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            sprite_path = os.path.join(project_root, 'assets', 'sprites', 'slime', animation.lower())

            frame_count = self.frame_counts[animation]
            for i in range(frame_count):
                img_path = os.path.join(sprite_path, f"{animation.capitalize()}_{i}.png")
                if animation.lower() == 'jump':
                    img_path = os.path.join(sprite_path, f"Jump_Land_{i}.png")
                if os.path.exists(img_path):
                    img = pygame.image.load(img_path).convert_alpha()
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)
            self.animation_list.append(temp_list if temp_list else [pygame.Surface((32, 32))])

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

    def move(self):
        dx = self.speed * self.direction
        dy = 0

        self.vel_y += 0.75
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        self.rect.x += dx
        self.check_collision('horizontal', dx)
        self.rect.y += dy
        self.check_collision('vertical', dy)

        if self.move_area:
            if self.rect.left < self.move_area.left:
                self.rect.left = self.move_area.left
                self.direction *= -1
                self.flip = not self.flip
            if self.rect.right > self.move_area.right:
                self.rect.right = self.move_area.right
                self.direction *= -1
                self.flip = not self.flip

        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600
            self.vel_y = 0
            self.in_air = False

        if not self.alive:
            return

    def check_collision(self, direction, move_value):
        map_width = self.battle_base.map_width
        map_height = self.battle_base.map_height
        tile_width = self.battle_base.tile_width
        tile_height = self.battle_base.tile_height
        tile_layers = self.battle_base.tile_layers
        layer = tile_layers[1]

        for row in range(map_height):
            for col in range(map_width):
                idx = row * map_width + col
                tile = layer[idx]
                if tile > 0:
                    tile_rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
                    if self.rect.colliderect(tile_rect):
                        if direction == 'horizontal':
                            if move_value > 0:
                                self.rect.right = tile_rect.left
                            elif move_value < 0:
                                self.rect.left = tile_rect.right
                        elif direction == 'vertical':
                            if move_value > 0:
                                self.rect.bottom = tile_rect.top
                                self.vel_y = 0
                                self.in_air = False
                            elif move_value < 0:
                                self.rect.top = tile_rect.bottom
                                self.vel_y = 0

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
            self.update_action(3)

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
