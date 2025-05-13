import pygame

class HealthBar:
    def __init__(self, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        self.font = pygame.font.SysFont('Arial', 18, bold=True)
        # Tạo icon trái tim (vector đơn giản)
        self.heart_surface = pygame.Surface((height, height), pygame.SRCALPHA)
        pygame.draw.polygon(self.heart_surface, (220, 20, 60), [
            (height//2, height-4),
            (4, height//2),
            (height//2, 4),
            (height-4, height//2)
        ])
        pygame.draw.circle(self.heart_surface, (220, 20, 60), (height//3, height//3), height//3)
        pygame.draw.circle(self.heart_surface, (220, 20, 60), (2*height//3, height//3), height//3)
=======
        self.font = pygame.font.SysFont('Arial', int(height * 0.8), bold=True)
>>>>>>> Stashed changes
=======
        self.font = pygame.font.SysFont('Arial', int(height * 0.8), bold=True)
>>>>>>> Stashed changes

    def set_health(self, health):
        self.current_health = max(0, min(self.max_health, health))

    def draw(self, surface):
        # Shadow
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        shadow_rect = pygame.Rect(self.x+6, self.y+6, self.width, self.height)
        pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=12)

        # Outer black outline
        outer_rect = pygame.Rect(self.x-2, self.y-2, self.width+4, self.height+4)
        pygame.draw.rect(surface, (0, 0, 0), outer_rect, border_radius=14)

        # White outline
        outline_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, border_radius=12)

        # Background
        bg_rect = pygame.Rect(self.x+3, self.y+3, self.width-6, self.height-6)
        pygame.draw.rect(surface, (40, 40, 40), bg_rect, border_radius=10)

        # Health bar (gradient)
        health_ratio = self.current_health / self.max_health
        health_width = int((self.width-6) * health_ratio)
        for i in range(health_width):
            # Gradient từ xanh lá sang vàng sang đỏ
            t = i / max(1, self.width-6)
            if t < 0.5:
                # Xanh lá sang vàng
=======
=======
>>>>>>> Stashed changes
        shadow_rect = pygame.Rect(self.x+4, self.y+4, self.width, self.height)
        pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=8)

        # Outer black outline
        outer_rect = pygame.Rect(self.x-1, self.y-1, self.width+2, self.height+2)
        pygame.draw.rect(surface, (0, 0, 0), outer_rect, border_radius=10)

        # White outline
        outline_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, border_radius=8)

        # Background
        bg_rect = pygame.Rect(self.x+2, self.y+2, self.width-4, self.height-4)
        pygame.draw.rect(surface, (40, 40, 40), bg_rect, border_radius=6)

        # Health bar (gradient)
        health_ratio = self.current_health / self.max_health
        health_width = int((self.width-4) * health_ratio)
        for i in range(health_width):
            t = i / max(1, self.width-4)
            if t < 0.5:
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
                r = int(50 + (255-50)*t*2)
                g = int(205 + (215-205)*t*2)
                b = int(50 - 50*t*2)
            else:
<<<<<<< Updated upstream
<<<<<<< Updated upstream
                # Vàng sang đỏ
                r = int(255 - (255-200)*(t-0.5)*2)
                g = int(215 - 215*(t-0.5)*2)
                b = 0
            pygame.draw.line(surface, (r, g, b), (self.x+3+i, self.y+3), (self.x+3+i, self.y+self.height-3), 1)
=======
=======
>>>>>>> Stashed changes
                r = int(255 - (255-200)*(t-0.5)*2)
                g = int(215 - 215*(t-0.5)*2)
                b = 0
            pygame.draw.line(surface, (r, g, b), (self.x+2+i, self.y+2), (self.x+2+i, self.y+self.height-2), 1)
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

        # Health text
        text = f"{int(self.current_health)}/{int(self.max_health)}"
        text_surf = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        # Viền chữ đen
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            shadow_rect = text_rect.move(dx, dy)
            surface.blit(self.font.render(text, True, (0,0,0)), shadow_rect)
        surface.blit(text_surf, text_rect)

<<<<<<< Updated upstream
<<<<<<< Updated upstream
        # Vẽ icon trái tim
        surface.blit(self.heart_surface, (self.x - self.height - 8, self.y))
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
