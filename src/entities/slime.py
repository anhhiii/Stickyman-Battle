import pygame
import os
from src.ai.algorithms import bfs_path, greedy_path, hill_climb_step, backtracking_path, q_learning_train, q_learning_step, and_or_search

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
        self.name = "slime_normal"
        self.q_table = None
        self.andor_path = []
        self.andor_index = 0
        self.bfs_path = []
        self.path_index = 0
        self.follow_player = False
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

    def update_bfs(self, player, grid):
        if not self.alive:
            return

        if abs(self.rect.centerx - player.rect.centerx) < 150:
            self.follow_player = True

        if self.follow_player:
            current_tile = (self.rect.centerx // self.battle_base.tile_width,
                            self.rect.centery // self.battle_base.tile_height)
            goal_tile = (player.rect.centerx // self.battle_base.tile_width,
                        player.rect.centery // self.battle_base.tile_height)

            if not self.bfs_path or self.path_index >= len(self.bfs_path):
                self.bfs_path = bfs_path(current_tile, goal_tile, grid)
                self.path_index = 0

            if self.bfs_path and self.path_index < len(self.bfs_path):
                tx, ty = self.bfs_path[self.path_index]
                target_x = tx * self.battle_base.tile_width
                if abs(self.rect.centerx - target_x) > 2:
                    if self.rect.centerx < target_x:
                        self.rect.x += self.speed
                        self.flip = False
                    elif self.rect.centerx > target_x:
                        self.rect.x -= self.speed
                        self.flip = True
                else:
                    self.path_index += 1
    def update_greedy(self, player, grid):
        if not self.alive:
            return

        if abs(self.rect.centerx - player.rect.centerx) < 150:
            self.follow_player = True

        if self.follow_player:
            current_tile = (self.rect.centerx // self.battle_base.tile_width,
                            self.rect.centery // self.battle_base.tile_height)
            goal_tile = (player.rect.centerx // self.battle_base.tile_width,
                        player.rect.centery // self.battle_base.tile_height)

            if not self.bfs_path or self.path_index >= len(self.bfs_path):
                self.bfs_path = greedy_path(current_tile, goal_tile, grid)
                self.path_index = 0

            if self.bfs_path and self.path_index < len(self.bfs_path):
                tx, ty = self.bfs_path[self.path_index]
                target_x = tx * self.battle_base.tile_width
                if abs(self.rect.centerx - target_x) > 2:
                    if self.rect.centerx < target_x:
                        self.rect.x += self.speed
                        self.flip = False
                    elif self.rect.centerx > target_x:
                        self.rect.x -= self.speed
                        self.flip = True
                else:
                    self.path_index += 1

    def update_hill_climb(self, player, grid):
        if not self.alive:
            return

        if abs(self.rect.centerx - player.rect.centerx) < 150:
            self.follow_player = True

        if self.follow_player:
            current_tile = (self.rect.centerx // self.battle_base.tile_width,
                            self.rect.centery // self.battle_base.tile_height)
            goal_tile = (player.rect.centerx // self.battle_base.tile_width,
                        player.rect.centery // self.battle_base.tile_height)

            next_tile = hill_climb_step(current_tile, goal_tile, grid)
            tx = next_tile[0] * self.battle_base.tile_width

            if abs(self.rect.centerx - tx) > 2:
                if self.rect.centerx < tx:
                    self.rect.x += self.speed
                    self.flip = False
                else:
                    self.rect.x -= self.speed
                    self.flip = True
    def update_backtracking(self, player, grid):
        if not self.alive:
            return

        if abs(self.rect.centerx - player.rect.centerx) < 150:
            self.follow_player = True

        if self.follow_player:
            current_tile = (self.rect.centerx // self.battle_base.tile_width,
                            self.rect.centery // self.battle_base.tile_height)
            goal_tile = (player.rect.centerx // self.battle_base.tile_width,
                        player.rect.centery // self.battle_base.tile_height)

            if not self.bfs_path or self.path_index >= len(self.bfs_path):
                self.bfs_path = backtracking_path(current_tile, goal_tile, grid)
                self.path_index = 0

            if self.bfs_path and self.path_index < len(self.bfs_path):
                tx, ty = self.bfs_path[self.path_index]
                target_x = tx * self.battle_base.tile_width

                if abs(self.rect.centerx - target_x) > 2:
                    if self.rect.centerx < target_x:
                        self.rect.x += self.speed
                        self.flip = False
                    elif self.rect.centerx > target_x:
                        self.rect.x -= self.speed
                        self.flip = True
                else:
                    self.path_index += 1

    def update_q_learning(self, player, grid):
        if not self.alive:
            return

        if abs(self.rect.centerx - player.rect.centerx) < 150:
            self.follow_player = True

        if self.follow_player:
            current_tile = (self.rect.centerx // self.battle_base.tile_width,
                            self.rect.centery // self.battle_base.tile_height)
            goal_tile = (player.rect.centerx // self.battle_base.tile_width,
                        player.rect.centery // self.battle_base.tile_height)

            if self.q_table is None:
                self.q_table = q_learning_train(grid, current_tile, goal_tile)

            next_tile = q_learning_step(self.q_table, current_tile)
            target_x = next_tile[0] * self.battle_base.tile_width

            if abs(self.rect.centerx - target_x) > 2:
                if self.rect.centerx < target_x:
                    self.rect.x += self.speed
                    self.flip = False
                elif self.rect.centerx > target_x:
                    self.rect.x -= self.speed
                    self.flip = True
    
    def update_andor(self, player, grid):
        if not self.alive:
            return
        if abs(self.rect.centerx - player.rect.centerx) < 150:
            self.follow_player = True

        if self.follow_player:
            current_tile = (self.rect.centerx // self.battle_base.tile_width,
                            self.rect.centery // self.battle_base.tile_height)
            goal_tile = (player.rect.centerx // self.battle_base.tile_width,
                        player.rect.centery // self.battle_base.tile_height)

            if not self.andor_path or self.andor_index >= len(self.andor_path):
                self.andor_path = and_or_search(current_tile, goal_tile, grid)
                self.andor_index = 0

            if self.andor_path and self.andor_index < len(self.andor_path):
                next_tile = self.andor_path[self.andor_index]
                target_x = next_tile[0] * self.battle_base.tile_width

                if abs(self.rect.centerx - target_x) > 2:
                    if self.rect.centerx < target_x:
                        self.rect.x += self.speed
                        self.flip = False
                    elif self.rect.centerx > target_x:
                        self.rect.x -= self.speed
                        self.flip = True
                else:
                    self.andor_index += 1

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
