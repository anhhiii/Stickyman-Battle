# Import class hoặc hàm từ các file trong thư mục khác
import pygame  # Thư viện game
import sys     # Để thoát chương trình
import os      # Để xử lý đường dẫn

# Import Background từ thư mục src/scenes
from src.scenes.background import Background
from src.scenes.menu import Menu

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("STICKY MAN")

    current_scene = "background"
    while True:
        if current_scene == "background":
            background = Background(screen)
            current_scene = background.run()

        elif current_scene == "menu":
            from src.scenes.menu import Menu
            menu_scene = Menu(screen)
            current_scene = menu_scene.run()

        elif current_scene == "quit":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
