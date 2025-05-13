import pygame
from src.scenes.battle_base import BattleBase
from src.components.music_manager import MusicManager
from src.entities.knight import Knight
from src.entities.slime import Slime
import os

class BattleLevel1(BattleBase):
    def __init__(self, screen):
        super().__init__(screen, level_name="level1")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        music_path = os.path.join(project_root, 'assets', 'audio', 'music_theme', 'MusicLV1.mp3')

        self.music_manager = MusicManager()
        self.music_manager.play_music(music_path)

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
                    move_area = pygame.Rect(x - 100, y - 50, 200, 100)  # phạm vi di chuyển riêng của mỗi slime
                    slime = Slime(x, y, 1.0, 2, self, move_area=move_area)
                    self.slime_list.append(slime)
                    print(f"[Slime] Spawned: {name} at {x}, {y}")

        if not self.player:
            raise ValueError("Không tìm thấy object 'player' trong map!")

        self.enemy_group = pygame.sprite.Group(self.slime_list)
        self.moving_left = False
        self.moving_right = False

        self.camera_offset = [0, 0]
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

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

            if self.player.alive:
                self.player.move(self.moving_left, self.moving_right)
                map_width_px = self.map_width * self.tile_width
                map_height_px = self.map_height * self.tile_height
                target_x = self.player.rect.centerx - self.screen_width // 2
                target_y = self.player.rect.centery - self.screen_height // 2
                self.camera_offset[0] = max(0, min(target_x, map_width_px - self.screen_width))
                self.camera_offset[1] = max(0, min(target_y, map_height_px - self.screen_height))

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

            self.draw()
            pygame.display.flip()
            clock.tick(60)

    def draw(self):
        self.screen.fill((0, 0, 0))
        super().draw(self.camera_offset)

        for sprite in self.player_group:
            flipped_image = pygame.transform.flip(sprite.image, sprite.flip, False)
            self.screen.blit(
                flipped_image,
                (sprite.rect.x - self.camera_offset[0], sprite.rect.y - self.camera_offset[1])
            )

        for sprite in self.enemy_group:
            self.screen.blit(
                sprite.image,
                (sprite.rect.x - self.camera_offset[0], sprite.rect.y - self.camera_offset[1])
            )

        bg_door = pygame.image.load("assets/backgrounds/BGDoor.png").convert_alpha()
        bg_door = pygame.transform.scale(bg_door, (64, 64))  # hoặc giữ nguyên
        pos_x = 64 - 64 - self.camera_offset[0]
        pos_y = 140 - self.camera_offset[1]
        self.screen.blit(bg_door, (pos_x, pos_y))

