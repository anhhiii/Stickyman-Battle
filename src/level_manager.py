import json
import os
from player import Player
from enemy import Enemy

class LevelManager:
    def __init__(self, level_file):
        """Khởi tạo level từ file JSON"""
        # Lấy đường dẫn tuyệt đối đến thư mục dự án
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        full_path = os.path.join(base_path, level_file)

        # Kiểm tra file tồn tại và load JSON
        try:
            with open(full_path, 'r') as file:
                self.level_data = json.load(file)
        except FileNotFoundError:
            print(f"⚠️ Lỗi: Không tìm thấy file level tại {full_path}")
            exit()
        except json.JSONDecodeError:
            print(f"⚠️ Lỗi: File {level_file} không đúng định dạng JSON!")
            exit()

        # Kiểm tra key bắt buộc trong JSON
        required_keys = ["player", "enemies", "rewards", "objective", "background"]
        for key in required_keys:
            if key not in self.level_data:
                print(f"⚠️ Lỗi: Thiếu key '{key}' trong file {level_file}")
                exit()

        # Khởi tạo các biến level
        self.player = None
        self.enemies = []
        self.background = self.level_data['background']
        self.rewards = self.level_data['rewards']
        self.objective = self.level_data['objective']

    def setup_level(self):
        """Tạo người chơi và quái từ dữ liệu trong level"""
        player_data = self.level_data['player']
        
        # Kiểm tra nếu thiếu "image" thì báo lỗi
        if "image" not in player_data:
            print("⚠️ Lỗi: Thiếu dữ liệu nhân vật: 'image'")
            exit()

        self.player = Player(
            player_data['spawn_x'],
            player_data['spawn_y'],
            player_data['hp'],
            player_data['weapon'],
            player_data['image']  # Đảm bảo truyền đúng đường dẫn ảnh
        )

        # Tạo quái vật từ dữ liệu JSON
        for enemy_data in self.level_data['enemies']:
            enemy = Enemy(
                enemy_data['type'],
                enemy_data['hp'],
                enemy_data['damage'],
                enemy_data['speed'],
                enemy_data['spawn_x'],
                enemy_data['spawn_y']
            )
            self.enemies.append(enemy)


    def check_victory(self):
        """Thắng khi không còn quái nào sống"""
        return all(enemy.hp <= 0 for enemy in self.enemies)

    def check_defeat(self):
        """Thua khi máu người chơi <= 0"""
        return self.player.hp <= 0

    def reward_player(self):
        """Trao thưởng khi thắng level"""
        if self.check_victory():
            print("🎉 Chúc mừng! Bạn đã hoàn thành level!")
            self.player.gold += self.rewards.get('gold', 0)
            self.player.exp += self.rewards.get('exp', 0)
            print(f"💰 Thưởng: {self.rewards.get('gold', 0)} vàng, {self.rewards.get('exp', 0)} EXP!")
        else:
            print("😢 Thua rồi! Thử lại nhé!")

