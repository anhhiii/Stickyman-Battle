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
        self.in_air = False
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
            sprite_path = os.path.join('assets/sprites/knight files/knight png/', animation)
            for i in range(6 if animation != 'Jump' else 2):
                img_path = os.path.join(sprite_path, f"{i}.png")
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def move(self, left, right):
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
            self.vel_y = -30
            self.jump = False
            self.in_air = True

        self.vel_y += 0.75
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        self.rect.x += dx
        self.check_collision('horizontal', dx)
        self.rect.y += dy
        self.check_collision('vertical', dy)
        #return dx

    def check_collision(self, direction, value):
        map_width = self.battle_base.map_width
        map_height = self.battle_base.map_height
        tile_width = self.battle_base.tile_width
        tile_height = self.battle_base.tile_height
        layer = self.battle_base.tile_layers[1]  # Ground layer

        for row in range(map_height):
            for col in range(map_width):
                idx = row * map_width + col
                tile = layer[idx]
                if tile > 0:
                    tile_rect = pygame.Rect(col * tile_width, row * tile_height, tile_width, tile_height)
                    if self.rect.colliderect(tile_rect):
                        if direction == 'horizontal':
                            if value > 0:
                                self.rect.right = tile_rect.left
                            elif value < 0:
                                self.rect.left = tile_rect.right
                        elif direction == 'vertical':
                            if value > 0:
                                self.rect.bottom = tile_rect.top
                                self.vel_y = 0
                                self.in_air = False
                            elif value < 0:
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
            self.update_action(3)  # Death

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
