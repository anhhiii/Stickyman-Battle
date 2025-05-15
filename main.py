# Import class hoặc hàm từ các file trong thư mục khác
import pygame  # Thư viện game
import sys     # Để thoát chương trình
import os      # Để xử lý đường dẫn




# Import Background từ thư mục src/scenes
from src.scenes.background import Background
from src.scenes.menu import Menu
from src.scenes.battle_level1 import BattleLevel1
from src.scenes.battle_level2 import BattleLevel2
from src.scenes.battle_level3 import BattleLevel3
from src.scenes.battle_boss import BattleBoss
<<<<<<< Updated upstream

=======
from src.ui.game_over import GameOverScreen
from src.ui.health_bar import HealthBar 
>>>>>>> Stashed changes

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((800, 608))
    pygame.display.set_caption("STICKY MAN")

<<<<<<< Updated upstream
=======
    # Khởi tạo thanh máu (góc trên bên trái)
    player_health = 100  
    health_bar = HealthBar(20, 20, 140, 20, player_health)  # x, y, width, height, max_health

>>>>>>> Stashed changes
    current_scene = "background"
    current_level = None  # Biến lưu màn chơi hiện tại
    while True:
        if current_scene == "background":
            background = Background(screen)
            current_scene = background.run()

        elif current_scene == "menu":
            from src.scenes.menu import Menu
            menu_scene = Menu(screen)
            current_scene = menu_scene.run()
        
<<<<<<< Updated upstream
        if current_scene == "level1":
            battle = BattleLevel1(screen)
            current_scene = battle.run()
=======
        elif current_scene == "level1":
            battle = BattleLevel1(screen, health_bar, player_health)
            result = battle.run()
            if isinstance(result, tuple) and result[0] == "game_over":
                current_scene = "game_over"
                current_level = result[1]  # Lưu màn chơi hiện tại
            else:
                current_scene = result

>>>>>>> Stashed changes
        elif current_scene == "level2":
            battle = BattleLevel2(screen)
            current_scene = battle.run()
        elif current_scene == "level3":
            battle = BattleLevel3(screen)
            current_scene = battle.run()
        elif current_scene == "boss":
            battle = BattleBoss(screen)
            current_scene = battle.run()
<<<<<<< Updated upstream


=======
        
        elif current_scene == "game_over":
            game_over_screen = GameOverScreen(screen, current_level)  # Truyền màn chơi hiện tại
            result = game_over_screen.run()
            if result == "restart":
                # Reset lại màn chơi hiện tại
                if current_level == "level1":
                    battle = BattleLevel1(screen, health_bar, player_health)
                    result = battle.run()
                    if isinstance(result, tuple) and result[0] == "game_over":
                        current_scene = "game_over"
                        current_level = result[1]
                    else:
                        current_scene = result
                elif current_level == "level2":
                    battle = BattleLevel2(screen, health_bar, player_health)
                    result = battle.run()
                    if isinstance(result, tuple) and result[0] == "game_over":
                        current_scene = "game_over"
                        current_level = result[1]
                    else:
                        current_scene = result
                elif current_level == "level3":
                    battle = BattleLevel3(screen, health_bar, player_health)
                    result = battle.run()
                    if isinstance(result, tuple) and result[0] == "game_over":
                        current_scene = "game_over"
                        current_level = result[1]
                    else:
                        current_scene = result
                elif current_level == "boss":
                    battle = BattleBoss(screen, health_bar, player_health)
                    result = battle.run()
                    if isinstance(result, tuple) and result[0] == "game_over":
                        current_scene = "game_over"
                        current_level = result[1]
                    else:
                        current_scene = result
            elif result == "menu":
                current_scene = "menu"
            elif result == "back":
                # Reset lại màn chơi hiện tại (giống logic "restart")
                if current_level == "level1":
                    battle = BattleLevel1(screen, health_bar, player_health)
                    result = battle.run()
                    if isinstance(result, tuple) and result[0] == "game_over":
                        current_scene = "game_over"
                        current_level = result[1]
                    else:
                        current_scene = result
                elif current_level == "level2":
                    battle = BattleLevel2(screen, health_bar, player_health)
                    result = battle.run()
                    if isinstance(result, tuple) and result[0] == "game_over":
                        current_scene = "game_over"
                        current_level = result[1]
                    else:
                        current_scene = result
                elif current_level == "level3":
                    battle = BattleLevel3(screen, health_bar, player_health)
                    result = battle.run()
                    if isinstance(result, tuple) and result[0] == "game_over":
                        current_scene = "game_over"
                        current_level = result[1]
                    else:
                        current_scene = result
                elif current_level == "boss":
                    battle = BattleBoss(screen, health_bar, player_health)
                    result = battle.run()
                    if isinstance(result, tuple) and result[0] == "game_over":
                        current_scene = "game_over"
                        current_level = result[1]
                    else:
                        current_scene = result
            elif result == "quit":
                pygame.quit()
                sys.exit()
>>>>>>> Stashed changes

        elif current_scene == "quit":
            pygame.quit()
            sys.exit()

if __name__ == "__main__": 
    main()