import pygame
from src.scenes.battle_base import BattleBase
from src.components.music_manager import MusicManager
from src.entities.knight import Knight
from src.entities.slime import Slime
from src.ui.settings_menu import SettingsMenu
from src.ui.game_over import GameOverScreen
from src.components.level_manager import LevelLogicManager
import os

class BattleLevel1(BattleBase):
    def __init__(self, screen, health_bar, player_health):
        super().__init__(screen, level_name="level1")
        self.screen = screen
        self.health_bar = health_bar
        self.player_health = player_health
        self.running = True
        self.paused = False
        self.door_pos = None
        self.player = None
        self.slime_list = []
        self.logic_manager = LevelLogicManager(self.slime_list)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        music_path = os.path.join(project_root, 'assets', 'audio', 'music_theme', 'MusicLV1.mp3')
        
        self.music_manager = MusicManager()
        self.music_manager.play_music(music_path)

        # Khởi tạo các đối tượng từ object layer
        BGDoor_dir = os.path.join(project_root, 'assets', 'backgrounds')
        self.BGDoor = pygame.image.load(os.path.join(BGDoor_dir, "BGDoor.png")).convert_alpha()
        self.BGDoor = pygame.transform.scale(self.BGDoor, (96, 96))

        for obj in self.spawn_objects:
            x = int(obj["x"])
            y = int(obj["y"])
            props = obj["properties"]
            
            if props.get("win") == "yes":
                self.door_pos = (obj["x"], obj["y"])
                print(f"[Door] Found at {self.door_pos}")


            if props.get("player") == "yes":
                self.player = Knight(x, y, scale=0.35, speed=3, battle_base=self)
                self.player_group = pygame.sprite.Group(self.player)
                print(f"[Knight] Spawned at {x}, {y}")
            elif props.get("enemy") == "yes":
                move_area = pygame.Rect(x - 100, y - 50, 200, 100)
                slime = Slime(x, y, 1.0, 2, self, move_area=move_area)
                self.slime_list.append(slime)
                print(f"[Slime] Spawned at {x}, {y}")

        if not self.player:
            raise ValueError("Không tìm thấy object 'player' trong map!")

        self.enemy_group = pygame.sprite.Group(self.slime_list)
        self.moving_left = False
        self.moving_right = False

        # Khởi tạo camera offset
        self.camera_offset = [0, 0]
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Khởi tạo các icon (giữ nguyên đường dẫn tương đối như yêu cầu)
        icon_dir = os.path.join(project_root, 'assets', 'icons')

        # Tải icon cài đặt
        self.settings_icon = pygame.image.load(os.path.join(icon_dir, "settings_icon.png"))
        self.settings_icon = pygame.transform.scale(self.settings_icon, (30, 30))
        self.settings_button = pygame.Rect(750, 10, 30, 30)

        # Tải icon Pause
        self.pause_icon = pygame.image.load(os.path.join(icon_dir, "pause_icon.png"))
        self.pause_icon = pygame.transform.scale(self.pause_icon, (30, 30))
        self.pause_button = pygame.Rect(700, 10, 30, 30)

        # Tải icon Continue
        self.continue_icon = pygame.image.load(os.path.join(icon_dir, "continue_icon.png"))
        self.continue_icon = pygame.transform.scale(self.continue_icon, (30, 30))
        self.continue_button = pygame.Rect(650, 10, 30, 30)

        



    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.logic_manager.update()

            if self.door_pos:
                door_rect = pygame.Rect(self.door_pos[0], self.door_pos[1], 32, 32)
                player_rect = self.player.rect.move(-self.camera_offset[0], -self.camera_offset[1])
                if self.logic_manager.check_victory(player_rect, door_rect):
                    return "win"
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    if not self.paused:
                        if event.key == pygame.K_a:
                            self.moving_left = True
                        if event.key == pygame.K_d:
                            self.moving_right = True
                        if event.key == pygame.K_w and self.player.alive:
                            self.player.jump = True
                        if event.key == pygame.K_SPACE and self.player.alive:
                            self.player.update_action(3)
                        if event.key == pygame.K_b:
                            self.player.block = True
                        if event.key == pygame.K_c:
                            self.player.cast = True
                        if event.key == pygame.K_s:
                            self.player.crouch = True
                        if event.key == pygame.K_e:
                            self.player.dash = True
                elif event.type == pygame.KEYUP:
                    if not self.paused:
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause_button.collidepoint(event.pos):
                        self.paused = True
                    elif self.continue_button.collidepoint(event.pos):
                        self.paused = False
                    elif self.settings_button.collidepoint(event.pos):
                        settings_menu = SettingsMenu(self.screen)
                        result = settings_menu.run()
                        if result == "menu":
                            return "menu"
                        elif result == "back":
                            continue

            if self.player.alive and not self.paused:
                self.player.move(self.moving_left, self.moving_right)
                map_width_px = self.map_width * self.tile_width
                map_height_px = self.map_height * self.tile_height

                target_x = self.player.rect.centerx - self.screen_width // 2
                target_y = self.player.rect.centery - self.screen_height // 2

                self.camera_offset[0] = max(0, min(target_x, map_width_px - self.screen_width))
                self.camera_offset[1] = max(0, min(target_y, map_height_px - self.screen_height))
                print(f"Camera offset: {self.camera_offset}, Player pos: {self.player.rect.centerx}, {self.player.rect.centery}")

                if self.player.attack and self.player.in_air:
                    self.player.update_action(10)
                elif self.player.attack:
                    if self.player.action != 3:
                        self.player.update_action(3)
                    for slime in self.slime_list:
                        if slime.alive and self.player.rect.colliderect(slime.rect):
                            slime.health -= 10
                            slime.update_action(2)
                            slime.check_alive()
                elif self.player.block:
                    self.player.update_action(4)
                elif self.player.cast:
                    self.player.update_action(5)
                elif self.player.crouch:
                    self.player.update_action(6)
                elif self.player.dash:
                    self.player.update_action(7)
                elif self.player.health <= 50 and not self.player.in_air:
                    self.player.update_action(8)
                elif self.player.health <= 70 and not self.player.in_air:
                    self.player.update_action(9)
                elif self.player.in_air and self.player.vel_y > 1:
                    self.player.update_action(2)
                elif self.moving_left or self.moving_right:
                    self.player.update_action(1)
                else:
                    self.player.update_action(0)

                self.player.update_animation()

            for slime in self.slime_list:
                if slime.alive:
                    slime.move()
                    if slime.in_air:
                        slime.update_action(1)
                    else:
                        slime.update_action(0)
                else:
                    if slime.action != 3:
                        slime.update_action(3)
                slime.update_animation()
                slime.check_alive()

            # Kiểm tra trạng thái sống của Knight và gọi GameOverScreen nếu chết
            if not self.player.alive:
                self.player_health = 0
                self.health_bar.set_health(self.player_health)
                game_over_screen = GameOverScreen(self.screen)
                result = game_over_screen.run()
                if result == "restart":
                    return "restart"
                elif result == "menu":
                    return "menu"
                elif result == "quit":
                    self.running = False
            else:
                self.player_health = self.player.health
                self.health_bar.set_health(self.player_health)

            self.draw()
            pygame.display.flip()
            clock.tick(60)

    def draw(self):
        self.screen.fill((0, 0, 0))
        super().draw(self.camera_offset)

        # ========== DEBUG: Vẽ các object trigger (gnd, wall) ==========
        debug_color_wall = (255, 0, 0)   # đỏ cho wall
        debug_color_gnd = (0, 255, 0)    # xanh lá cho gnd

        for obj in self.wall_objects:
            rect = pygame.Rect(
                obj["x"] - self.camera_offset[0],
                obj["y"] - self.camera_offset[1],
                obj["width"],
                obj["height"]
            )
            pygame.draw.rect(self.screen, debug_color_wall, rect, 2)

        for obj in self.ground_objects:
            rect = pygame.Rect(
                obj["x"] - self.camera_offset[0],
                obj["y"] - self.camera_offset[1],
                obj["width"],
                obj["height"]
            )
            pygame.draw.rect(self.screen, debug_color_gnd, rect, 2)
        
        # DEBUG: Vẽ khung slime
        for slime in self.slime_list:
            pygame.draw.rect(
                self.screen,
                (255, 255, 0),  # màu vàng
                pygame.Rect(
                    slime.rect.x - self.camera_offset[0],
                    slime.rect.y - self.camera_offset[1],
                    slime.rect.width,
                    slime.rect.height
                ),
                2
            )
        for slime in self.slime_list:
            detect_range = 96  # Đồng bộ với detect_range trong SlimeAI
            detection_rect = pygame.Rect(
                slime.rect.centerx - detect_range - self.camera_offset[0],
                slime.rect.centery - 32 - self.camera_offset[1],
                detect_range * 2,
                64
            )
            pygame.draw.rect(self.screen, (255, 255, 255), detection_rect, 1)  # khung trắng
        # =============================================================

        if self.door_pos:
            door_x = self.door_pos[0] - self.camera_offset[0]
            door_y = self.door_pos[1] - self.BGDoor.get_height() - self.camera_offset[1]
            print(f"[DRAW] BGDoor at screen coords: {door_x}, {door_y}")
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(door_x, door_y, 64, 64), 2)  # Vẽ khung để dễ thấy
            self.screen.blit(self.BGDoor, (door_x, door_y))

        for sprite in self.player_group:
            flipped_image = pygame.transform.flip(sprite.image, sprite.flip, False)
            self.screen.blit(flipped_image, (sprite.rect.x - self.camera_offset[0], sprite.rect.y - self.camera_offset[1]))

        for sprite in self.enemy_group:
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


        