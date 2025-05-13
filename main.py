import pygame  # Thư viện game
import sys     # Để thoát chương trình
import os      # Để xử lý đường dẫn

# Import các lớp từ thư mục src/scenes
from src.scenes.background import Background
from src.scenes.menu import Menu
from src.scenes.battle_level1 import BattleLevel1
from src.scenes.battle_level2 import BattleLevel2
from src.scenes.battle_level3 import BattleLevel3
from src.scenes.battle_boss import BattleBoss
from src.ui.health_bar import HealthBar  

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((800, 608))
    pygame.display.set_caption("STICKY MAN")

    # Khởi tạo thanh máu (góc trên bên trái)
    player_health = 100  # Giá trị máu ban đầu
    health_bar = HealthBar(20, 20, 140, 20, player_health)  # x, y, width, height, max_health

    current_scene = "background"
    while True:
        if current_scene == "background":
            background = Background(screen)
            current_scene = background.run()

        elif current_scene == "menu":
            menu_scene = Menu(screen)
            current_scene = menu_scene.run()
        
        elif current_scene == "level1":
            battle = BattleLevel1(screen, health_bar, player_health)  
            current_scene = battle.run()
        elif current_scene == "level2":
            battle = BattleLevel2(screen, health_bar, player_health)  
            current_scene = battle.run()
        elif current_scene == "level3":
            battle = BattleLevel3(screen, health_bar, player_health)  
            current_scene = battle.run()
        elif current_scene == "boss":
            battle = BattleBoss(screen, health_bar, player_health) 
            current_scene = battle.run()
        
        elif current_scene == "quit":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()