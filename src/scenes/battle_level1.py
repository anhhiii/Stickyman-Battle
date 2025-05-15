import pygame
import time  # Thêm thư viện để xử lý delay
from src.scenes.battle_base import BattleBase
from src.components.music_manager import MusicManager
from src.entities.knight import Knight
from src.entities.slime import Slime
from src.ai.algorithms import bfs_path

import os

class BattleLevel1(BattleBase):
    def __init__(self, screen):
        super().__init__(screen, level_name="level1")
<<<<<<< Updated upstream
=======
        self.screen = screen
        self.health_bar = health_bar
        self.player_health = player_health
        self.running = True
        self.paused = False
        self.door_pos = None
        self.player = None
        self.slime_list = []
        self.logic_manager = LevelLogicManager(self.slime_list)
        self.slime_attack_delay = 5.0  # Thời gian delay sau khi slime tấn công (3 giây)
        self.knight_run_delay = 5.0  # Thời gian knight chạy trước khi slime tấn công lại (3 giây)
        self.last_attack_time = 0  # Thời gian tấn công cuối cùng của slime
        self.knight_running = False  # Trạng thái knight đang chạy
        self.knight_run_start_time = 0  # Thời gian bắt đầu chạy của knight
>>>>>>> Stashed changes

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        music_path = os.path.join(project_root, 'assets', 'audio', 'music_theme', 'MusicLV1.mp3')
        
        self.music_manager = MusicManager()
        self.music_manager.play_music(music_path)

        # Khởi tạo các đối tượng từ object layer
        self.player = None
        self.slime_list = []
        for layer in self.object_layers:
            for obj in layer:
                name = obj.get("name", "").lower()
                x = int(obj["x"])
                y = int(obj["y"])

                if name == "player":
                    self.player = Knight(x, y, scale=0.35, speed=3, battle_base=self)
                    self.player_group = pygame.sprite.Group(self.player)
                    print(f"[Knight] Spawned at {x}, {y}")
                elif "slime" in name:
                    slime = Slime(x, y, 1.0, 2, self, name=name)
                    self.slime_list.append(slime)
                    print(f"[Slime] Spawned: {name} at {x}, {y}")

        if not self.player:
            raise ValueError("Không tìm thấy object 'player' trong map!")

        self.enemy_group = pygame.sprite.Group(self.slime_list)
        self.moving_left = False
        self.moving_right = False

        # Khởi tạo camera offset
        self.camera_offset = [0, 0]  # [x, y]
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
<<<<<<< Updated upstream
=======
            current_time = time.time()
            self.logic_manager.update()

            if self.door_pos:
                door_rect = pygame.Rect(self.door_pos[0], self.door_pos[1], 32, 32)
                player_rect = self.player.rect.move(-self.camera_offset[0], -self.camera_offset[1])
                if self.logic_manager.check_victory(player_rect, door_rect):
                    return "win"
                
>>>>>>> Stashed changes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                    if event.key == pygame.K_a:
                        self.moving_left = True
                    if event.key == pygame.K_d:
                        self.moving_right = True
                    if event.key == pygame.K_w and self.player.alive:
                        self.player.jump = True
                    if event.key == pygame.K_SPACE and self.player.alive:
                        self.player.update_action(3)  # Kích hoạt Attack
                    if event.key == pygame.K_b:
                        self.player.block = True
                    if event.key == pygame.K_c:
                        self.player.cast = True
                    if event.key == pygame.K_s:
                        self.player.crouch = True
                    if event.key == pygame.K_e:
                        self.player.dash = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.moving_left = False
                    if event.key == pygame.K_d:
                        self.moving_right = False
                    if event.key == pygame.K_b:
                        self.player.block = False
                    if event.key == pygame.K_c:
                        self.player.cast = False
                    if event.key == pygame.K_s:
                        self.player.crouch = False
                    if event.key == pygame.K_e:
                        self.player.dash = False

<<<<<<< Updated upstream
            if self.player.alive:
=======
            # Logic tấn công của slime
            if self.slime_is_near_knight():  # Kiểm tra nếu slime gần knight
                if not self.knight_running and current_time - self.last_attack_time >= self.slime_attack_delay:
                    self.knight_take_damage()  # Knight bị thương
                    self.knight_running = True  # Knight bắt đầu chạy
                    self.knight_run_start_time = current_time  # Ghi lại thời gian bắt đầu chạy

            # Logic knight chạy
            if self.knight_running:
                if current_time - self.knight_run_start_time >= self.knight_run_delay:
                    self.knight_running = False  # Knight dừng chạy
                    self.last_attack_time = current_time  # Cập nhật thời gian tấn công cuối cùng
                    self.slime_continue_moving()  # Slime tiếp tục di chuyển

            if self.player.alive and not self.paused:
                # Di chuyển nhân vật
>>>>>>> Stashed changes
                self.player.move(self.moving_left, self.moving_right)
                map_width_px = self.map_width * self.tile_width
                map_height_px = self.map_height * self.tile_height

                target_x = self.player.rect.centerx - self.screen_width // 2
                target_y = self.player.rect.centery - self.screen_height // 2

                # Điều chỉnh camera để di chuyển tự do theo chiều dọc
                self.camera_offset[0] = max(0, min(target_x, map_width_px - self.screen_width))
                self.camera_offset[1] = max(0, min(target_y, map_height_px - self.screen_height))
                print(f"Camera offset: {self.camera_offset}, Player pos: {self.player.rect.centerx}, {self.player.rect.centery}, Map height: {map_height_px}")

                # Đồng bộ với self.animation_types trong Knight
                if self.player.attack and self.player.in_air:
                    self.player.update_action(10)  # JumpAttack
                elif self.player.attack:
                    if self.player.action != 3:
                        self.player.update_action(3)   # Attack
                    for slime in self.slime_list:
                        if slime.alive and self.player.rect.colliderect(slime.rect):
                            slime.health -= 10
                            slime.update_action(2)  # Hurt
                            slime.check_alive()
                elif self.player.block:
                    self.player.update_action(4)   # Block
                elif self.player.cast:
                    self.player.update_action(5)   # Cast
                elif self.player.crouch:
                    self.player.update_action(6)   # Crouch
                elif self.player.dash:
                    self.player.update_action(7)   # Dash
                elif self.player.health <= 50 and not self.player.in_air:
                    self.player.update_action(8)   # Dizzy
                elif self.player.health <= 70 and not self.player.in_air:
                    self.player.update_action(9)   # Hurt
                elif self.player.in_air and self.player.vel_y > 1:
                    self.player.update_action(2)   # Jump
                elif self.moving_left or self.moving_right:
                    self.player.update_action(1)   # Walk
                else:
                    self.player.update_action(0)   # Idle

                self.player.update_animation()

            for slime in self.slime_list:
                if slime.alive:
                    slime.move()
                    if slime.in_air:
                        slime.update_action(1)  # Jump
                    else:
<<<<<<< Updated upstream
                        slime.update_action(0)  # Idle
                else:
                    if slime.action != 3:
                        slime.update_action(3)  # Death
                slime.update_animation()
                slime.check_alive()
=======
                        if slime.action != 3:
                            slime.update_action(3)
                    slime.update_animation()
                    slime.check_alive()

                # Trong vòng lặp trò chơi chính, thêm xử lý va chạm giữa Slime và nhân vật
                for slime in self.slime_list:
                    if slime.alive:
                        # Kiểm tra va chạm giữa Slime và nhân vật
                        if slime.rect.colliderect(self.player.rect):
                            if self.player.health > 0:
                                self.player.health -= 1  
                                self.health_bar.set_health(self.player.health)  # Cập nhật thanh máu
                            if self.player.health <= 0:
                                self.player.alive = False  # Đặt trạng thái nhân vật là chết
                                self.player.health = 0
                                self.health_bar.set_health(0)  # Đảm bảo thanh máu về 0
                                break  # Thoát khỏi vòng lặp nếu nhân vật chết

            # Kiểm tra trạng thái sống của Knight và gọi GameOverScreen nếu chết
            if not self.player.alive:
                return "game_over", "level1"  # Trả về "game_over" và màn chơi hiện tại

            self.player_health = self.player.health
            self.health_bar.set_health(self.player_health)
>>>>>>> Stashed changes

            self.draw()
            pygame.display.flip()
            clock.tick(60)

    def slime_is_near_knight(self):
        """Kiểm tra nếu slime gần knight."""
        # Thêm logic kiểm tra khoảng cách giữa slime và knight
        return True  # Thay bằng điều kiện thực tế

    def knight_take_damage(self):
        """Knight bị thương khi slime tấn công."""
        self.player_health -= 10  # Giảm máu của knight
        self.health_bar.set_health(self.player_health)  # Cập nhật thanh máu

    def slime_continue_moving(self):
        """Slime tiếp tục di chuyển sau khi tấn công."""
        # Thêm logic để slime tiếp tục di chuyển
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))  # Xóa màn hình
        super().draw(self.camera_offset)

        # Vẽ Knight với camera offset và flip đúng
        for sprite in self.player_group:
            print(f"Drawing Knight: flip={sprite.flip}, pos={sprite.rect.x}, {sprite.rect.y}")  # Debug
            flipped_image = pygame.transform.flip(sprite.image, sprite.flip, False)
            self.screen.blit(
                flipped_image,
                (sprite.rect.x - self.camera_offset[0], sprite.rect.y - self.camera_offset[1])
            )

        # Vẽ enemy với camera offset
        for sprite in self.enemy_group:
<<<<<<< Updated upstream
            self.screen.blit(
                sprite.image,
                (sprite.rect.x - self.camera_offset[0], sprite.rect.y - self.camera_offset[1])
            )
=======
            self.screen.blit(sprite.image, (sprite.rect.x - self.camera_offset[0], sprite.rect.y - self.camera_offset[1]))

        self.health_bar.draw(self.screen)

        self.screen.blit(self.settings_icon, (self.settings_button.x, self.settings_button.y))
        self.screen.blit(self.pause_icon, (self.pause_button.x, self.pause_button.y))
        self.screen.blit(self.continue_icon, (self.continue_button.x, self.continue_button.y))


        if self.paused:
            font = pygame.font.SysFont('Arial', 36, bold=True)
            pause_text = font.render("PAUSED", True, (255, 255, 255))
            text_rect = pause_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(pause_text, text_rect)

        pygame.draw.rect(self.screen, (0, 255, 255), (
        self.player.rect.x - self.camera_offset[0],
        self.player.rect.y - self.camera_offset[1],
        self.player.rect.width,
        self.player.rect.height
), 2)


>>>>>>> Stashed changes
