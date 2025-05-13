# src/scenes/background.py

import pygame
import os

class Background:
    def __init__(self, screen):
        self.screen = screen
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = screen.get_size()
        
        # Game state
        self.running = True
        
        # Load background image
        current_dir = os.path.dirname(os.path.abspath(__file__))  # scenes folder
        project_root = os.path.dirname(os.path.dirname(current_dir))  # Stickyman-Battle folder
        bg_path = os.path.join(project_root, 'assets', 'backgrounds', '1.jpg')
        try:
            self.original_bg_image = pygame.image.load(bg_path)
            self.update_background_size()
        except FileNotFoundError:
            print(f"Could not find background image at: {bg_path}")
            print("Current working directory:", os.getcwd())
            raise
            
        # Load fonts from assets/fonts
        try:
            title_font_path = os.path.join(project_root, 'assets', 'fonts', 'RubikGlitch-Regular.ttf')
            text_font_path = os.path.join(project_root, 'assets', 'fonts', 'Hexenkoetel-qZRv1.ttf')
            
            self.title_font = pygame.font.Font(title_font_path, 74)
            self.text_font = pygame.font.Font(text_font_path, 36)
        except FileNotFoundError:
            print("Could not find font files. Using default fonts.")
            self.title_font = pygame.font.Font(None, 74)
            self.text_font = pygame.font.Font(None, 36)
    
    def update_background_size(self):
        """Cập nhật kích thước background theo kích thước màn hình"""
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = self.screen.get_size()
        self.bg_image = pygame.transform.scale(self.original_bg_image, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
    
    def draw_background(self, screen):
        # Draw background image
        screen.blit(self.bg_image, (0, 0))
    
    def draw_text(self, screen):
        # Draw title "STICKY MAN"
        title_text = self.title_font.render("STICKY MAN", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 4))
        
        # Add shadow effect to title
        shadow_text = self.title_font.render("STICKY MAN", True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(self.WINDOW_WIDTH // 2 + 4, self.WINDOW_HEIGHT // 4 + 4))
        
        # Draw "Start new journey"
        start_text = self.text_font.render("Start new journey", True, (0, 0, 0))
        start_rect = start_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2))
        
        # Draw texts
        screen.blit(shadow_text, shadow_rect)
        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to start
                    # Add game start logic here
                    pass
                
                # Toggle fullscreen with F11
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                    self.update_background_size()
    
    def run(self):
        clock = pygame.time.Clock()
        
        while self.running:
            self.handle_events()
            self.draw_background(self.screen)
            self.draw_text(self.screen)
            pygame.display.flip()
            clock.tick(60)
