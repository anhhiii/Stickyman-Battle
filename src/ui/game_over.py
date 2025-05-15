import pygame
import os

class GameOverScreen:
    def __init__(self, screen, current_level):
        self.screen = screen
        self.current_level = current_level  # Lưu màn chơi hiện tại
        self.running = True

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Tải font Rubik Glitch
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))  # Lên 2 cấp để đến thư mục gốc
        font_path = os.path.join(project_root, "assets", "fonts", "RubikGlitch-Regular.ttf")
        
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")
        
        self.font_game_over = pygame.font.Font(font_path, 72)  # Font Rubik Glitch, kích thước 72

        # Tạo chữ "GAME OVER"
        self.game_over_text = self.font_game_over.render("GAME OVER", True, (255, 0, 0))  # Màu đỏ
        self.game_over_rect = self.game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 3))

        # Tạo khung Game Over (nhỏ hơn và màu vàng)
        self.overlay_rect = pygame.Rect(0, 0, 250, 120)  # Kích thước khung nhỏ hơn
        self.overlay_rect.center = (self.screen_width // 2, self.screen_height // 2 + 50)

        # Tải icon nút Back và Menu
        icon_dir = os.path.join(project_root, "assets", "icons")
        self.back_icon = pygame.image.load(os.path.join(icon_dir, "back_icon.png"))
        self.back_icon = pygame.transform.scale(self.back_icon, (50, 50))
        self.back_button = self.back_icon.get_rect(center=(self.overlay_rect.centerx - 60, self.overlay_rect.centery))

        self.menu_icon = pygame.image.load(os.path.join(icon_dir, "home_icon.png"))
        self.menu_icon = pygame.transform.scale(self.menu_icon, (50, 50))
        self.menu_button = self.menu_icon.get_rect(center=(self.overlay_rect.centerx + 60, self.overlay_rect.centery))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.collidepoint(event.pos):
                        self.running = False
                        return "back"  # Trả về "back" để reset màn chơi
                    elif self.menu_button.collidepoint(event.pos):
                        self.running = False
                        return "menu"  # Quay về menu

            self.draw()
            pygame.display.flip()

    def draw(self):

        # Vẽ khung màu vàng
        pygame.draw.rect(self.screen, (255, 255, 0), self.overlay_rect, border_radius=15)  # Viền vàng
        pygame.draw.rect(self.screen, (255, 255, 200), self.overlay_rect.inflate(-8, -8), border_radius=15)  # Nền vàng nhạt

        # Vẽ chữ "GAME OVER"
        self.screen.blit(self.game_over_text, self.game_over_rect)

        # Vẽ nút Back và Menu
        self.screen.blit(self.back_icon, self.back_button.topleft)
        self.screen.blit(self.menu_icon, self.menu_button.topleft)