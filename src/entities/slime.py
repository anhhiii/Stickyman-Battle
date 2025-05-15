import pygame
import os
from src.ai.algorithms import bfs_path, greedy_path, hill_climb_step, backtracking_path, q_learning_train, q_learning_step, and_or_search
import random

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
        self.q_table_trained = False
        self.hill_stuck_counter = 0

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
    
    def _is_target_changed(self, new_goal_tile):
        if not hasattr(self, 'last_goal_tile'):
            return True
        return abs(new_goal_tile[0] - self.last_goal_tile[0]) > 1 or abs(new_goal_tile[1] - self.last_goal_tile[1]) > 1

    def update_bfs(self, player, grid, margin_data):
        if not self.alive:
            return

        # Kiểm tra khoảng cách đến người chơi
        if abs(self.rect.centerx - player.rect.centerx) < 150:
            self.follow_player = True
        else:
            self.follow_player = False
            self.bfs_path = []
            self.path_index = 0
            return

        if self.follow_player:
            current_tile = (self.rect.centerx // self.battle_base.tile_width,
                            self.rect.centery // self.battle_base.tile_height)
            goal_tile = (player.rect.centerx // self.battle_base.tile_width,
                        player.rect.centery // self.battle_base.tile_height)

            if not self.bfs_path or self.path_index >= len(self.bfs_path) or self._is_target_changed(goal_tile):
                self.bfs_path = bfs_path(current_tile, goal_tile, grid)
                self.path_index = 0
                self.last_goal_tile = goal_tile

            if self.bfs_path and self.path_index < len(self.bfs_path):
                tx, ty = self.bfs_path[self.path_index]
                target_x = tx * self.battle_base.tile_width + self.battle_base.tile_width // 2

                # Kiểm tra biên từ lớp margin
                if (0 <= ty < self.battle_base.map_height and 0 <= tx < self.battle_base.map_width):
                    margin_index = ty * self.battle_base.map_width + tx
                    if margin_index < len(margin_data) and margin_data[margin_index] != 0:
                        self.direction *= -1  # Quay đầu
                        self.rect.x += self.direction * self.speed  # Điều chỉnh vị trí
                        print(f"[DEBUG] Slime at {self.rect.centerx}, {self.rect.centery} hit margin at {tx}, {ty}")
                    else:
                        if abs(self.rect.centerx - target_x) > self.speed:
                            if self.rect.centerx < target_x:
                                self.rect.x += self.speed
                                self.flip = False
                                self.direction = 1
                            else:
                                self.rect.x -= self.speed
                                self.flip = True
                                self.direction = -1
                            self.check_collision('horizontal', self.speed * self.direction)
                        else:
                            self.path_index += 1
                self.update_action(1 if self.in_air or abs(self.rect.centerx - target_x) > self.speed else 0)

    def update_greedy(self, player, grid, margin_data):
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

                # Kiểm tra biên từ lớp margin
                if (0 <= ty < self.battle_base.map_height and 0 <= tx < self.battle_base.map_width):
                    margin_index = ty * self.battle_base.map_width + tx
                    if margin_index < len(margin_data) and margin_data[margin_index] != 0:
                        self.direction *= -1  # Quay đầu
                        self.rect.x += self.direction * self.speed  # Điều chỉnh vị trí
                    else:
                        if abs(self.rect.centerx - target_x) > 2:
                            if self.rect.centerx < target_x:
                                self.rect.x += self.speed
                                self.flip = False
                            elif self.rect.centerx > target_x:
                                self.rect.x -= self.speed
                                self.flip = True
                        else:
                            self.path_index += 1

    def update_hill_climb(self, player, grid, margin_data):
        if not self.alive:
            return

        if abs(self.rect.centerx - player.rect.centerx) < 150:
            self.follow_player = True
        else:
            self.follow_player = False
            return

        if self.follow_player:
            current_tile = (self.rect.centerx // self.battle_base.tile_width,
                            self.rect.centery // self.battle_base.tile_height)
            goal_tile = (player.rect.centerx // self.battle_base.tile_width,
                        player.rect.centery // self.battle_base.tile_height)

            if not hasattr(self, 'hill_stuck_counter'):
                self.hill_stuck_counter = 0

            next_tile = hill_climb_step(current_tile, goal_tile, grid)
            current_h = abs(current_tile[0] - goal_tile[0]) + abs(current_tile[1] - goal_tile[1])
            next_h = abs(next_tile[0] - goal_tile[0]) + abs(next_tile[1] - goal_tile[1])

            if next_h >= current_h:
                self.hill_stuck_counter += 1
            else:
                self.hill_stuck_counter = 0

            if self.hill_stuck_counter > 10:
                valid_moves = []
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = current_tile[0] + dx, current_tile[1] + dy
                    if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and grid[ny][nx] == 0:
                        valid_moves.append((nx, ny))
                if valid_moves:
                    next_tile = random.choice(valid_moves)
                self.hill_stuck_counter = 0

            tx = next_tile[0] * self.battle_base.tile_width + self.battle_base.tile_width // 2
            if (0 <= next_tile[1] < self.battle_base.map_height and 0 <= next_tile[0] < self.battle_base.map_width):
                margin_index = next_tile[1] * self.battle_base.map_width + next_tile[0]
                if margin_index < len(margin_data) and margin_data[margin_index] != 0:
                    self.direction *= -1  # Quay đầu
                    self.rect.x += self.direction * self.speed  # Điều chỉnh vị trí
                else:
                    if abs(self.rect.centerx - tx) > self.speed:
                        if self.rect.centerx < tx:
                            self.rect.x += self.speed
                            self.flip = False
                            self.direction = 1
                        else:
                            self.rect.x -= self.speed
                            self.flip = True
                            self.direction = -1
                        self.check_collision('horizontal', self.speed * self.direction)
            self.update_action(1 if self.in_air or abs(self.rect.centerx - tx) > self.speed else 0)

    def update_backtracking(self, player, grid, margin_data):
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

                # Kiểm tra biên từ lớp margin
                if (0 <= ty < self.battle_base.map_height and 0 <= tx < self.battle_base.map_width):
                    margin_index = ty * self.battle_base.map_width + tx
                    if margin_index < len(margin_data) and margin_data[margin_index] != 0:
                        self.direction *= -1  # Quay đầu
                        self.rect.x += self.direction * self.speed  # Điều chỉnh vị trí
                    else:
                        if abs(self.rect.centerx - target_x) > 2:
                            if self.rect.centerx < target_x:
                                self.rect.x += self.speed
                                self.flip = False
                            elif self.rect.centerx > target_x:
                                self.rect.x -= self.speed
                                self.flip = True
                        else:
                            self.path_index += 1

    def update_q_learning(self, player, grid, margin_data):
        if not self.alive:
            return

        if abs(self.rect.centerx - player.rect.centerx) < 150:
            self.follow_player = True
        else:
            self.follow_player = False
            return

        if self.follow_player:
            current_tile = (self.rect.centerx // self.battle_base.tile_width,
                            self.rect.centery // self.battle_base.tile_height)
            goal_tile = (player.rect.centerx // self.battle_base.tile_width,
                        player.rect.centery // self.battle_base.tile_height)

            if not self.q_table_trained:
                self.q_table = q_learning_train(grid, current_tile, goal_tile, episodes=100)
                self.q_table_trained = True

            next_tile = q_learning_step(self.q_table, current_tile)
            target_x = next_tile[0] * self.battle_base.tile_width + self.battle_base.tile_width // 2

            # Kiểm tra biên từ lớp margin
            if (0 <= next_tile[1] < self.battle_base.map_height and 0 <= next_tile[0] < self.battle_base.map_width):
                margin_index = next_tile[1] * self.battle_base.map_width + next_tile[0]
                if margin_index < len(margin_data) and margin_data[margin_index] != 0:
                    self.direction *= -1  # Quay đầu
                    self.rect.x += self.direction * self.speed  # Điều chỉnh vị trí
                else:
                    if abs(self.rect.centerx - target_x) > self.speed:
                        if self.rect.centerx < target_x:
                            self.rect.x += self.speed
                            self.flip = False
                            self.direction = 1
                        else:
                            self.rect.x -= self.speed
                            self.flip = True
                            self.direction = -1
                        self.check_collision('horizontal', self.speed * self.direction)
            self.update_action(1 if self.in_air or abs(self.rect.centerx - target_x) > self.speed else 0)
    
    def update_andor(self, player, grid, margin_data):
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

                # Kiểm tra biên từ lớp margin
                if (0 <= next_tile[1] < self.battle_base.map_height and 0 <= next_tile[0] < self.battle_base.map_width):
                    margin_index = next_tile[1] * self.battle_base.map_width + next_tile[0]
                    if margin_index < len(margin_data) and margin_data[margin_index] != 0:
                        self.direction *= -1  # Quay đầu
                        self.rect.x += self.direction * self.speed  # Điều chỉnh vị trí
                    else:
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
        if not self.alive:
            return  # Không di chuyển nếu slime đã chết

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

    def check_collision(self, direction, move_value):
        tile_width = self.battle_base.tile_width
        tile_height = self.battle_base.tile_height
        layer = self.battle_base.tile_layers[1]
        map_width = self.battle_base.map_width

        col_left = max(0, (self.rect.left - tile_width) // tile_width)
        col_right = min(self.battle_base.map_width - 1, (self.rect.right + tile_width) // tile_width)
        row_top = max(0, (self.rect.top - tile_height) // tile_height)
        row_bottom = min(self.battle_base.map_height - 1, (self.rect.bottom + tile_height) // tile_height)

        for row in range(row_top, row_bottom + 1):
            for col in range(col_left, col_right + 1):
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
            if self.action == 3:  # Nếu là Death thì giữ frame cuối
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
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