import pygame
from src.scenes.battle_base import BattleBase
from src.components.music_manager import MusicManager
from src.entities.knight import Knight
import os

class BattleLevel1(BattleBase):
    def __init__(self, screen):
        super().__init__(screen, level_name="level1")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        music_path = os.path.join(project_root, 'assets', 'audio', 'music_theme', 'MusicLV1.mp3')
        
        self.music_manager = MusicManager()
        self.music_manager.play_music(music_path)
        # Điều chỉnh vị trí khởi tạo: đứng trên sàn chính
        self.player = Knight(200, 336, 0.5, 5, self)  # scale=0.5, y=336 để đứng trên sàn y=464
        self.player_group = pygame.sprite.Group(self.player)
        self.moving_left = False
        self.moving_right = False
        print("Level started with knight at:", self.player.rect.topleft)

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
                    if event.key == pygame.K_SPACE:
                        self.player.load_sprite('Attack')
                        self.player.attack = True
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
                    if event.key == pygame.K_SPACE:
                        self.player.attack = False
                    if event.key == pygame.K_b:
                        self.player.block = False
                    if event.key == pygame.K_c:
                        self.player.cast = False
                    if event.key == pygame.K_s:
                        self.player.crouch = False
                    if event.key == pygame.K_e:
                        self.player.dash = False

            if self.player.alive:
                if self.player.attack and self.player.in_air:
                    self.player.update_action(11)  # JumpAttack
                elif self.player.attack:
                    self.player.update_action(4)   # Attack
                elif self.player.block:
                    self.player.update_action(5)   # Block
                elif self.player.cast:
                    self.player.update_action(6)   # Cast
                elif self.player.crouch:
                    self.player.update_action(7)   # Crouch
                elif self.player.dash:
                    self.player.update_action(8)   # Dash
                elif self.player.health <= 50 and not self.player.in_air:
                    self.player.update_action(9)   # Dizzy
                elif self.player.health <= 70 and not self.player.in_air:
                    self.player.update_action(10)  # Hurt
                elif self.player.in_air:
                    self.player.update_action(2)   # Jump
                elif self.moving_left or self.moving_right:
                    self.player.update_action(1)   # Walk
                else:
                    self.player.update_action(0)   # Idle

                self.player.move(self.moving_left, self.moving_right)
                print("Knight position after move:", self.player.rect.topleft)

            self.player.update_animation()
            self.player.check_alive()
            self.draw()
            self.player_group.draw(self.screen)
            pygame.display.flip()
            clock.tick(60)

    def draw(self):
        super().draw()  # Vẽ bản đồ từ BattleBase