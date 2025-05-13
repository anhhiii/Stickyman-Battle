import pygame
import os

class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Khởi tạo font
        self.font_game_over = pygame.font.SysFont('Arial', 72, bold=True)
        
        # Tạo chữ "GAME OVER"
        self.game_over_text = self.font_game_over.render("GAME OVER", True, (255, 215, 0))  # Màu vàng
        self.game_over_rect = self.game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 3))

        # Tạo khung Game Over
        self.overlay_rect = pygame.Rect(self.screen_width // 4, self.screen_height // 2, self.screen_width // 2, self.screen_height // 4)
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        icon_dir = os.path.join(project_root, 'assets', 'icons')

        # Tải icon "Back"
        self.back_icon = pygame.image.load(os.path.join(icon_dir, "back_icon.png"))
        self.back_icon = pygame.transform.scale(self.back_icon, (100, 50))
        self.back_button = pygame.Rect(self.screen_width // 2 - 120, self.screen_height // 2 + 20, 100, 50)

        # Tải icon "Home"
        self.home_icon = pygame.image.load(os.path.join(icon_dir, "home_icon.png"))
        self.home_icon = pygame.transform.scale(self.home_icon, (100, 50))
        self.home_button = pygame.Rect(self.screen_width // 2 + 20, self.screen_height // 2 + 20, 100, 50)

        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.collidepoint(event.pos):
                        self.running = False
                        return "restart"  # Khởi động lại level
                    elif self.home_button.collidepoint(event.pos):
                        self.running = False
                        return "menu"  # Quay về menu

            self.draw()
            pygame.display.flip()

    def draw(self):
        # Vẽ chữ "GAME OVER" màu vàng
        self.screen.blit(self.game_over_text, self.game_over_rect)

        # Vẽ icon "Back"
        self.screen.blit(self.back_icon, (self.back_button.x, self.back_button.y))

        # Vẽ icon "Home"
        self.screen.blit(self.home_icon, (self.home_button.x, self.home_button.y))