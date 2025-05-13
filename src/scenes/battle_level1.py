import pygame
from src.scenes.battle_base import BattleBase
from src.components.music_manager import MusicManager
from src.entities.knight import Knight
from src.entities.slime import Slime
from src.ui.settings_menu import SettingsMenu  # Import lớp SettingsMenu
import os
import sys

class BattleLevel1(BattleBase):
    def __init__(self, screen, health_bar, player_health):
        super().__init__(screen, level_name="level1")
        self.screen = screen
        self.health_bar = health_bar
        self.player_health = player_health
        self.running = True
        self.paused = False  # Trạng thái tạm dừng

        self.running = True
        self.paused = False  # Trạng thái tạm dừng

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
                    self.player = Knight(x, y, scale=0.35, speed=5, battle_base=self)
                    self.player_group = pygame.sprite.Group(self.player)
                    print(f"[Knight] Spawned at {x}, {y}")
                elif "slime" in name:
                    slime = Slime(x, y, 1.0, 2, self)
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

        # Tải icon cài đặt
        self.settings_icon = pygame.image.load("assets/icons/settings_icon.png")
        self.settings_icon = pygame.transform.scale(self.settings_icon, (30, 30))  # Resize icon nhỏ hơn
        self.settings_button = pygame.Rect(750, 10, 30, 30)  # Vị trí và kích thước nút Settings

        # Tải icon Pause
        self.pause_icon = pygame.image.load("assets/icons/pause_icon.png")
        self.pause_icon = pygame.transform.scale(self.pause_icon, (30, 30))  # Resize icon nhỏ hơn
        self.pause_button = pygame.Rect(700, 10, 30, 30)  # Vị trí và kích thước nút Pause

        # Tải icon Continue
        self.continue_icon = pygame.image.load("assets/icons/continue_icon.png")
        self.continue_icon = pygame.transform.scale(self.continue_icon, (30, 30))  # Resize icon nhỏ hơn
        self.continue_button = pygame.Rect(650, 10, 30, 30)  # Vị trí và kích thước nút Continue

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                    if event.key == pygame.K_p:  # Nhấn phím P để tạm dừng
                        self.paused = not self.paused  # Đảo trạng thái tạm dừng
                    if not self.paused:  # Chỉ xử lý các phím khác khi không tạm dừng
                        if event.key == pygame.K_a:
                            self.moving_left = True
                        if event.key == pygame.K_d:
                            self.moving_right = True
                        if event.key == pygame.K_w and self.player.alive:
                            self.player.jump = True
                        if event.key == pygame.K_SPACE:
                            self.player.load_sprite('Attack')
                            self.player.attack = True
                elif event.type == pygame.KEYUP:
                    if not self.paused:  # Chỉ xử lý khi không tạm dừng
                        if event.key == pygame.K_a:
                            self.moving_left = False
                        if event.key == pygame.K_d:
                            self.moving_right = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Xử lý nút Pause
                    if self.pause_button.collidepoint(event.pos):
                        self.paused = True
                    # Xử lý nút Continue
                    elif self.continue_button.collidepoint(event.pos):
                        self.paused = False
                    # Xử lý nút Settings
                    if self.settings_button.collidepoint(event.pos):
                        settings_menu = SettingsMenu(self.screen)
                        result = settings_menu.run()
                        if result == "menu":
                            return "menu"  # Quay lại menu chính
                        elif result == "back":
                            continue  # Quay lại màn chơi

            if not self.paused:
                if self.player.alive:
                    self.player.move(self.moving_left, self.moving_right)

                    # Cập nhật camera offset
                    map_width_px = self.map_width * self.tile_width
                    map_height_px = self.map_height * self.tile_height

                    target_x = self.player.rect.centerx - self.screen_width // 2
                    target_y = self.player.rect.centery - self.screen_height // 2

                    self.camera_offset[0] = max(0, min(target_x, map_width_px - self.screen_width))
                    self.camera_offset[1] = max(0, min(target_y, map_height_px - self.screen_height))

                # Cập nhật slime
                for slime in self.slime_list:
                    if slime.alive:
                        slime.move()
                    slime.update_animation()
                    slime.check_alive()

                # Kiểm tra va chạm với slime
                if pygame.sprite.spritecollide(self.player, self.enemy_group, False):
                    self.player_health -= self.health_bar.max_health / 3  # Trừ 1/3 máu
                    self.health_bar.set_health(self.player_health)
                    if self.player_health <= 0:
                        self.player.alive = False  # Nhân vật chết

                # Kiểm tra nếu nhân vật rơi ra khỏi màn hình
                if self.player.rect.top > self.screen.get_height():
                    self.player_health = 0
                    self.health_bar.set_health(self.player_health)
                    self.player.alive = False  # Nhân vật chết

            # Vẽ màn hình
            self.draw()
            pygame.display.flip()
            clock.tick(60)

    def draw(self):
        # Xóa màn hình
        self.screen.fill((0, 0, 0))

        # Vẽ bản đồ và các đối tượng
        super().draw(self.camera_offset)

        # Vẽ nhóm nhân vật và kẻ thù
        self.player_group.draw(self.screen)
        self.enemy_group.draw(self.screen)

        # Vẽ thanh máu
        self.health_bar.draw(self.screen)

        # Vẽ icon Settings
        self.screen.blit(self.settings_icon, (self.settings_button.x, self.settings_button.y))

        # Vẽ icon Pause
        self.screen.blit(self.pause_icon, (self.pause_button.x, self.pause_button.y))

        # Vẽ icon Continue
        self.screen.blit(self.continue_icon, (self.continue_button.x, self.continue_button.y))
       
        # Hiển thị thông báo tạm dừng
        if self.paused:
            font = pygame.font.SysFont('Arial', 36, bold=True)
            pause_text = font.render("PAUSED", True, (255, 255, 255))
            text_rect = pause_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(pause_text, text_rect)