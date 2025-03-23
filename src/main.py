import pygame
import sys
import os

# Khởi tạo Pygame
pygame.init()

# Cấu hình cửa sổ
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickyman Battle")

# Lấy thư mục gốc của dự án
base_path = os.path.dirname(__file__)
background_path = os.path.join(base_path, "..", "assets", "backgrounds", "1.jpg")
background = pygame.image.load(background_path)

background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Khởi tạo font
base_path = os.path.dirname(__file__)  # Lấy đường dẫn thư mục hiện tại của file main.py
title_font_path = os.path.join(base_path, "..", "assets", "fonts", "RubikGlitch-Regular.ttf")
title_font = pygame.font.Font(title_font_path, 80)

menu_font_path = os.path.join(base_path, "..", "assets", "fonts", "CourierPrime-Regular.ttf")
menu_font = pygame.font.Font(menu_font_path, 40)

# Hàm vẽ văn bản
def draw_text(text, font, color, surface, x, y):
    """Vẽ chữ lên màn hình."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Hàm tạo menu chính
def main_menu():
    """Hiển thị menu chính."""
    while True:
        screen.blit(background, (0, 0))
        draw_text("STICK MAN", title_font, (255, 0, 0), screen, WIDTH // 2, HEIGHT // 3)
        draw_text("Start new journey", menu_font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 2)

        pygame.display.flip()

        # Xử lý sự kiện trong menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # Thoát menu và vào game

# Hàm chính của game
def game_loop():
    """Vòng lặp game chính."""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Chạy game
main_menu()  # Bắt đầu từ menu
game_loop()  # Sau đó vào game
