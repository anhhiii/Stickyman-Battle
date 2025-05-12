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
                    self.player.in_air = False
                    self.player_group = pygame.sprite.Group(self.player)
                    print(f"[Knight] Spawned at {x}, {y}")
                elif "slime" in name:
                    slime = Slime(x, y, 1.0, 2, self)
                    self.slime_list.append(slime)
                    print(f"[Slime] Spawned: {name} at {x}, {y}")

        # Kiểm tra đảm bảo player đã tạo
        if not self.player:
            raise ValueError("Không tìm thấy object 'player' trong map!")

        self.enemy_group = pygame.sprite.Group(self.slime_list)
        self.moving_left = False
        self.moving_right = False



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

            if self.player.alive:
                if self.player.attack and self.player.in_air:
                    self.player.update_action(11)  # JumpAttack
                elif self.player.attack:
                    if self.player.action != 4:
                        self.player.update_action(4)   # Attack
                    # Kiểm tra va chạm giữa Knight và từng Slime
                    for slime in self.slime_list:
                        if slime.alive and self.player.rect.colliderect(slime.rect):
                            slime.health -= 10
                            slime.update_action(2)  # Hurt
                            slime.check_alive()
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
                elif self.player.in_air and self.player.vel_y > 1:
                    self.player.update_action(2)   # Jump
                elif self.moving_left or self.moving_right:
                    self.player.update_action(1)   # Walk
                else:
                    self.player.update_action(0)   # Idle

                self.player.move(self.moving_left, self.moving_right)

            # Cập nhật Slimes
            for slime in self.slime_list:
                if slime.alive:
                    slime.move()
                    if slime.in_air:
                        slime.update_action(1)  # Jump
                    else:
                        slime.update_action(0)  # Idle
                else:
                    if slime.action != 3:
                        slime.update_action(3)  # Death
                slime.update_animation()
                slime.check_alive()

            self.player.update_animation()
            self.player.check_alive()

            self.draw()
            self.player_group.draw(self.screen)
            self.enemy_group.draw(self.screen)
            pygame.display.flip()
            clock.tick(60)


    def draw(self):
        super().draw()  # Vẽ bản đồ từ BattleBase