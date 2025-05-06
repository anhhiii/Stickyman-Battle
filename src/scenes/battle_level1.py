from src.scenes.battle_base import BattleBase
from src.components.music_manager import MusicManager
import os

class BattleLevel1(BattleBase):
    def __init__(self, screen):
        super().__init__(screen, level_name="level1")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        music_path = os.path.join(project_root, 'assets', 'audio', 'music_theme', 'MusicLV1.mp3')
        
        self.music_manager = MusicManager()
        self.music_manager.play_music(music_path)
