import pygame
import os
from src.ai.algorithms import bfs_path, greedy_path, hill_climb_step, backtracking_path, q_learning_train, q_learning_step, and_or_search_probabilistic
from src.ai.platform_graph import find_nearest_node
import random

class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, battle_base, move_area=None, navigation_mode="platform"):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.direction = -1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
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
        self.last_goal_node = None
        self.navigation_mode = navigation_mode
        self.frame_counts = {
            'Idle': 7,
            'Jump': 6,
            'Hurt': 11,
            'Death': 14
        }
        self.q_table_trained = False
        self.hill_stuck_counter = 0
        self.is_attacking = False
        self.last_attack_time = 0
        self.attack_cooldown = 2000
        self.death_animation_complete = False
        self.platform_nodes = self.battle_base.platform_nodes
        self.platform_graph = self.battle_base.platform_graph
        self.jump_strength = -18
        self.jump_cooldown = 200
        self.last_jump_time = 0

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
                else:
                    print(f"[Slime] WARNING: Image not found at {img_path}")
                    temp_list.append(pygame.Surface((32, 32)))
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

    def _is_target_changed(self, new_goal):
        return self.last_goal_node != new_goal if self.last_goal_node is not None else True

    def try_jump(self):
        current_time = pygame.time.get_ticks()
        if not self.in_air and current_time - self.last_jump_time > self.jump_cooldown:
            self.vel_y = self.jump_strength
            self.in_air = True
            self.jump = True
            self.last_jump_time = current_time
            self.update_action(1)
            print(f"[Slime] {self.name} jumped at {self.rect.centerx}, {self.rect.centery}")

    def try_attack_player(self, player):
        current_time = pygame.time.get_ticks()
        if self.rect.colliderect(player.rect) and current_time - getattr(player, 'last_hurt_time', 0) > 1000 and \
           current_time - self.last_attack_time > self.attack_cooldown:
            player.health -= 10
            player.is_hurt = True
            player.update_action(8)
            player.last_hurt_time = current_time
            print(f"[{self.name}] Slime attacked! Knight health: {player.health}")
            self.last_attack_time = current_time
            if player.health <= 0:
                player.check_alive()

    def move_to_node(self, target_x, target_y):
        slime_x, slime_y = self.rect.center
        height_diff = slime_y - target_y
        dist_x = abs(slime_x - target_x)
        if dist_x > 3:
            if target_x < slime_x:
                self.rect.x -= self.speed
                self.flip = True
                self.direction = -1
            else:
                self.rect.x += self.speed
                self.flip = False
                self.direction = 1
            self.check_collision('horizontal', self.speed * self.direction)
            print(f"[Slime] {self.name} moving to ({target_x}, {target_y}), dist_x={dist_x}")
            return False, dist_x
        else:
            if height_diff > 10 and not self.in_air:
                self.try_jump()
            elif height_diff < -20 and not self.in_air:
                pass
            else:
                return True, dist_x
        return False, dist_x

    def update_bfs(self, player):
        if not self.alive:
            return
        dist_to_player = ((self.rect.centerx - player.rect.centerx) ** 2 + (self.rect.centery - player.rect.centery) ** 2) ** 0.5
        self.follow_player = dist_to_player < 500
        if not self.follow_player:
            self.bfs_path = []
            self.path_index = 0
            self.update_action(0)
            print(f"[Slime {self.name}] Player too far, stopping, dist={dist_to_player}")
            return
        slime_x, slime_y = self.rect.center
        knight_x, knight_y = player.rect.center
        slime_node = find_nearest_node(slime_x, slime_y, self.platform_nodes)
        knight_node = find_nearest_node(knight_x, knight_y, self.platform_nodes)
        if slime_node is None or knight_node is None:
            print(f"[Platform BFS] Cannot find nodes: slime_node={slime_node}, knight_node={knight_node}")
            self.update_action(0)
            return
        print(f"[Slime {self.name}] Slime node: {slime_node}, Knight node: {knight_node}")
        if not self.bfs_path or self.path_index >= len(self.bfs_path) or self._is_target_changed(knight_node):
            self.bfs_path = bfs_path(slime_node, knight_node, self.platform_graph)
            self.path_index = 0
            self.last_goal_node = knight_node
            print(f"[Slime {self.name}] BFS path: {self.bfs_path}")
        if self.bfs_path and self.path_index < len(self.bfs_path):
            next_node_idx = self.bfs_path[self.path_index]
            next_node = self.platform_nodes[next_node_idx]
            target_x, target_y = next_node['center']
            reached, dist_x = self.move_to_node(target_x, target_y)
            if reached:
                self.path_index += 1
                print(f"[Slime {self.name}] Reached node {next_node_idx}, moving to next")
            self.update_action(1 if self.in_air or dist_x > 3 else 0)
        else:
            print(f"[Slime {self.name}] No valid BFS path or path completed")
            self.update_action(0)
        self.try_attack_player(player)

    def update_greedy(self, player):
        if not self.alive:
            return
        dist_to_player = ((self.rect.centerx - player.rect.centerx) ** 2 + (self.rect.centery - player.rect.centery) ** 2) ** 0.5
        self.follow_player = dist_to_player < 500
        if not self.follow_player:
            self.bfs_path = []
            self.path_index = 0
            self.update_action(0)
            print(f"[Slime {self.name}] Player too far, stopping, dist={dist_to_player}")
            return
        slime_x, slime_y = self.rect.center
        knight_x, knight_y = player.rect.center
        slime_node = find_nearest_node(slime_x, slime_y, self.platform_nodes)
        knight_node = find_nearest_node(knight_x, knight_y, self.platform_nodes)
        if slime_node is None or knight_node is None:
            print(f"[Platform Greedy] Cannot find nodes: slime_node={slime_node}, knight_node={knight_node}")
            self.update_action(0)
            return
        print(f"[Slime {self.name}] Slime node: {slime_node}, Knight node: {knight_node}")
        if not self.bfs_path or self.path_index >= len(self.bfs_path) or self._is_target_changed(knight_node):
            self.bfs_path = greedy_path(slime_node, knight_node, self.platform_graph, self.platform_nodes)
            self.path_index = 0
            self.last_goal_node = knight_node
            print(f"[Slime {self.name}] Greedy path: {self.bfs_path}")
        if self.bfs_path and self.path_index < len(self.bfs_path):
            next_node_idx = self.bfs_path[self.path_index]
            next_node = self.platform_nodes[next_node_idx]
            target_x, target_y = next_node['center']
            reached, dist_x = self.move_to_node(target_x, target_y)
            if reached:
                self.path_index += 1
                print(f"[Slime {self.name}] Reached node {next_node_idx}, moving to next")
            self.update_action(1 if self.in_air or dist_x > 3 else 0)
        else:
            print(f"[Slime {self.name}] No valid Greedy path or path completed")
            self.update_action(0)
        self.try_attack_player(player)

    def update_hill_climb(self, player):
        if not self.alive:
            return
        dist_to_player = ((self.rect.centerx - player.rect.centerx) ** 2 + (self.rect.centery - player.rect.centery) ** 2) ** 0.5
        self.follow_player = dist_to_player < 500
        if not self.follow_player:
            self.update_action(0)
            print(f"[Slime {self.name}] Player too far, stopping, dist={dist_to_player}")
            return
        slime_x, slime_y = self.rect.center
        knight_x, knight_y = player.rect.center
        slime_node = find_nearest_node(slime_x, slime_y, self.platform_nodes)
        knight_node = find_nearest_node(knight_x, knight_y, self.platform_nodes)
        if slime_node is None or knight_node is None:
            print(f"[Platform Hill Climb] Cannot find nodes: slime_node={slime_node}, knight_node={knight_node}")
            self.update_action(0)
            return
        print(f"[Slime {self.name}] Slime node: {slime_node}, Knight node: {knight_node}")
        next_node = hill_climb_step(slime_node, knight_node, self.platform_graph, self.platform_nodes)
        next_node_data = self.platform_nodes[next_node]
        target_x, target_y = next_node_data['center']
        reached, dist_x = self.move_to_node(target_x, target_y)
        self.update_action(1 if self.in_air or dist_x > 3 else 0)
        self.try_attack_player(player)

    def update_backtracking(self, player):
        if not self.alive:
            return
        dist_to_player = ((self.rect.centerx - player.rect.centerx) ** 2 + (self.rect.centery - player.rect.centery) ** 2) ** 0.5
        self.follow_player = dist_to_player < 500
        if not self.follow_player:
            self.bfs_path = []
            self.path_index = 0
            self.update_action(0)
            print(f"[Slime {self.name}] Player too far, stopping, dist={dist_to_player}")
            return
        slime_x, slime_y = self.rect.center
        knight_x, knight_y = player.rect.center
        slime_node = find_nearest_node(slime_x, slime_y, self.platform_nodes)
        knight_node = find_nearest_node(knight_x, knight_y, self.platform_nodes)
        if slime_node is None or knight_node is None:
            print(f"[Platform Backtracking] Cannot find nodes: slime_node={slime_node}, knight_node={knight_node}")
            self.update_action(0)
            return
        print(f"[Slime {self.name}] Slime node: {slime_node}, Knight node: {knight_node}")
        if not self.bfs_path or self.path_index >= len(self.bfs_path) or self._is_target_changed(knight_node):
            self.bfs_path = backtracking_path(slime_node, knight_node, self.platform_graph, self.platform_nodes)
            self.path_index = 0
            self.last_goal_node = knight_node
            print(f"[Slime {self.name}] Backtracking path: {self.bfs_path}")
        if self.bfs_path and self.path_index < len(self.bfs_path):
            next_node_idx = self.bfs_path[self.path_index]
            next_node = self.platform_nodes[next_node_idx]
            target_x, target_y = next_node['center']
            reached, dist_x = self.move_to_node(target_x, target_y)
            if reached:
                self.path_index += 1
                print(f"[Slime {self.name}] Reached node {next_node_idx}, moving to next")
            self.update_action(1 if self.in_air or dist_x > 3 else 0)
        else:
            print(f"[Slime {self.name}] No valid Backtracking path or path completed")
            self.update_action(0)
        self.try_attack_player(player)

    def update_q_learning(self, player):
        if not self.alive:
            return
        dist_to_player = ((self.rect.centerx - player.rect.centerx) ** 2 + (self.rect.centery - player.rect.centery) ** 2) ** 0.5
        self.follow_player = dist_to_player < 500
        if not self.follow_player:
            self.q_table = None
            self.update_action(0)
            print(f"[Slime {self.name}] Player too far, stopping, dist={dist_to_player}")
            return
        slime_x, slime_y = self.rect.center
        knight_x, knight_y = player.rect.center
        slime_node = find_nearest_node(slime_x, slime_y, self.platform_nodes)
        knight_node = find_nearest_node(knight_x, knight_y, self.platform_nodes)
        if slime_node is None or knight_node is None:
            print(f"[Platform Q-Learning] Cannot find nodes: slime_node={slime_node}, knight_node={knight_node}")
            self.update_action(0)
            return
        print(f"[Slime {self.name}] Slime node: {slime_node}, Knight node: {knight_node}")
        if not self.q_table or self._is_target_changed(knight_node):
            self.q_table = q_learning_train(self.platform_graph, slime_node, knight_node, nodes=self.platform_nodes)
            self.q_table_trained = True
            self.last_goal_node = knight_node
            print(f"[Slime {self.name}] Q-table trained for goal {knight_node}")
        next_node = q_learning_step(self.q_table, slime_node)
        next_node_data = self.platform_nodes[next_node]
        target_x, target_y = next_node_data['center']
        reached, dist_x = self.move_to_node(target_x, target_y)
        self.update_action(1 if self.in_air or dist_x > 3 else 0)
        self.try_attack_player(player)

    def update_andor(self, player):
        if not self.alive:
            return
        dist_to_player = ((self.rect.centerx - player.rect.centerx) ** 2 + (self.rect.centery - player.rect.centery) ** 2) ** 0.5
        self.follow_player = dist_to_player < 500
        if not self.follow_player:
            self.andor_path = []
            self.andor_index = 0
            self.update_action(0)
            print(f"[Slime {self.name}] Player too far, stopping, dist={dist_to_player}")
            return
        slime_x, slime_y = self.rect.center
        knight_x, knight_y = player.rect.center
        slime_node = find_nearest_node(slime_x, slime_y, self.platform_nodes)
        knight_node = find_nearest_node(knight_x, knight_y, self.platform_nodes)
        if slime_node is None or knight_node is None:
            print(f"[Platform AND-OR] Cannot find nodes: slime_node={slime_node}, knight_node={knight_node}")
            self.update_action(0)
            return
        print(f"[Slime {self.name}] Slime node: {slime_node}, Knight node: {knight_node}")
        if not self.andor_path or self.andor_index >= len(self.andor_path) or self._is_target_changed(knight_node):
            self.andor_path = and_or_search_probabilistic(slime_node, knight_node, self.platform_graph, self.platform_nodes)
            self.andor_index = 0
            self.last_goal_node = knight_node
            print(f"[Slime {self.name}] AND-OR path: {self.andor_path}")
        if self.andor_path and self.andor_index < len(self.andor_path):
            next_node_idx = self.andor_path[self.andor_index]
            next_node = self.platform_nodes[next_node_idx]
            target_x, target_y = next_node['center']
            reached, dist_x = self.move_to_node(target_x, target_y)
            if reached:
                self.andor_index += 1
                print(f"[Slime {self.name}] Reached node {next_node_idx}, moving to next")
            self.update_action(1 if self.in_air or dist_x > 3 else 0)
        else:
            print(f"[Slime {self.name}] No valid AND-OR path or path completed")
            self.update_action(0)
        self.try_attack_player(player)

    def move(self):
        if not self.alive:
            return
        dx = self.speed * self.direction
        dy = 0
        self.vel_y += 0.75
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        temp_rect = self.rect.move(dx, dy)
        if self.move_area and not self.move_area.contains(temp_rect):
            if temp_rect.left < self.move_area.left or temp_rect.right > self.move_area.right:
                self.direction *= -1
                dx = self.speed * self.direction
            temp_rect = self.rect.move(dx, dy)
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
        if self.rect.bottom > 608:
            self.rect.bottom = 608
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
                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                    self.death_animation_complete = True
                    print(f"[Slime] {self.name} completed Death animation")
                else:
                    self.frame_index = 0
            print(f"[Slime] {self.name} action={self.action}, frame={self.frame_index}")

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            self.death_animation_complete = False
            print(f"[Slime] {self.name} updated action to {new_action}")

    def check_alive(self):
        self.health = 0
        self.speed = 0
        self.alive = False
        self.update_action(3)
        print(f"[Slime] {self.name} triggered check_alive, switching to Death")

    def draw(self, screen):
        if self.alive or self.action == 3:
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
            print(f"[Slime] {self.name} drawn at {self.rect.x}, {self.rect.y}, action={self.action}")