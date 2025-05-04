import pygame
import os
import math
from src.components.settings_button import SettingsButton

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.exit_to_start = False  # Flag báo hiệu quay lại start game
        self.settings_button = SettingsButton(self.screen)


        self.font = pygame.font.SysFont("Stickyman-Battle/assets/fonts/CourierPrime-Regular.ttf", 100)

        # --- Load ảnh nền ---
        self.load_background()

        # --- Init mũi tên điều hướng (tọa độ tạm) ---
        self.arrow_left = pygame.Rect(0, 0, 50, 50)
        self.arrow_right = pygame.Rect(0, 0, 50, 50)

        # --- Danh sách màn chơi ---
        self.levels = [
            {"id": 1, "unlocked": True},
            {"id": 2, "unlocked": False},
            {"id": 3, "unlocked": False},
            {"id": 4, "unlocked": False},
        ]

        # --- Tạo nút và cập nhật kích thước ---
        self.buttons = []
        self.update_layout()

        # --- Load ảnh ổ khóa ---
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))

        lock_path = os.path.join(project_root, 'assets', 'icons', 'lock.png')
        self.lock_image = pygame.image.load(lock_path).convert_alpha()

        # # --- Load ảnh nút level ---
        self.button_image = pygame.Surface((140, 140), pygame.SRCALPHA)
        self.button_image.fill((0, 150, 255))  # màu xanh làm nút tạm

        # button_path = os.path.join(project_root, 'assets', 'icons', 'button.png')
        # self.button_image = pygame.image.load(button_path).convert_alpha()



    def draw_title(self):

        # Hiệu ứng lắc nhẹ
        frame = pygame.time.get_ticks() / 100
        offset = int(5 * math.sin(frame))

        # Font và kích cỡ
        font_size = max(80, self.WINDOW_HEIGHT // 7)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        title_font_path = os.path.join(project_root, 'assets', 'fonts', 'RubikGlitch-Regular.ttf')
        title_font = pygame.font.Font(title_font_path, font_size)

        # Text chính và bóng
        title_text = title_font.render("MENU", True, (255, 50, 50))      # Đỏ tươi
        shadow_text = title_font.render("MENU", True, (0, 0, 0))         # Bóng đen

        # Vị trí
        title_rect = title_text.get_rect(center=(self.WINDOW_WIDTH // 2, 70))
        shadow_rect = shadow_text.get_rect(center=(title_rect.centerx + 4, title_rect.centery + 4))

        # Vẽ
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(title_text, title_rect)



    def load_background(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        menu_path = os.path.join(project_root, 'assets', 'backgrounds', '6.png')
        try:
            self.original_bg_image = pygame.image.load(menu_path)
        except FileNotFoundError:
            print(f"Không tìm thấy ảnh nền tại: {menu_path}")
            raise

    def update_font_size(self):
        size = max(40, self.WINDOW_HEIGHT // 12)
        try:
            self.font = pygame.font.Font(os.path.join("assets", "fonts", "CourierPrime-Regular.ttf"), size)
        except:
            self.font = pygame.font.SysFont(None, size)


    def update_layout(self):
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = self.screen.get_size()
        self.bg_image = pygame.transform.scale(self.original_bg_image, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.arrow_left.topleft = (50, self.WINDOW_HEIGHT // 2 - 25)
        self.arrow_right.topleft = (self.WINDOW_WIDTH - 100, self.WINDOW_HEIGHT // 2 - 25)
        self.create_buttons()

    def create_buttons(self):
        button_w, button_h = 140, 140
        gap = 20
        grid_cols, grid_rows = 2, 2

        total_width = grid_cols * button_w + (grid_cols - 1) * gap
        total_height = grid_rows * button_h + (grid_rows - 1) * gap

        start_x = (self.WINDOW_WIDTH - total_width) // 2
        start_y = (self.WINDOW_HEIGHT - total_height) // 2

        self.buttons.clear()
        for i in range(grid_cols * grid_rows):
            col = i % grid_cols
            row = i // grid_cols
            x = start_x + col * (button_w + gap)
            y = start_y + row * (button_h + gap)
            self.buttons.append(pygame.Rect(x, y, button_w, button_h))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.arrow_left.collidepoint(event.pos):
                    print("← Quay lại màn hình start game")
                    self.exit_to_start = True
                    self.running = False


                elif self.arrow_right.collidepoint(event.pos):
                    print("→ Tiếp trang (chưa xử lý logic)")

                for i, rect in enumerate(self.buttons):
                    if rect.collidepoint(event.pos):
                        if self.levels[i]["unlocked"]:
                            print(f"Bắt đầu màn {self.levels[i]['id']}")
                        else:
                            print("Màn này chưa mở!")


    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # Vẽ các nút level
        for i, rect in enumerate(self.buttons):
            level = self.levels[i]
            is_hover = rect.collidepoint(pygame.mouse.get_pos())

            if level["unlocked"]:
                # Nút nền có màu sáng hơn khi hover
                color = (80, 220, 80) if not is_hover else (120, 255, 120)
                pygame.draw.rect(self.screen, color, rect, border_radius=10)

                # Hiện số level
                text = self.font.render(str(level["id"]), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
            else:
                # Vẽ nền xám + hình ổ khóa
                pygame.draw.rect(self.screen, (180, 180, 180), rect, border_radius=10)
                lock_scaled = pygame.transform.smoothscale(self.lock_image, (rect.width, rect.height))
                self.screen.blit(lock_scaled, rect.topleft)

        # Vẽ khung bao quanh cụm nút
        if self.buttons:
            margin = 20
            left = self.buttons[0].left - margin
            top = self.buttons[0].top - margin
            right = self.buttons[-1].right + margin
            bottom = self.buttons[-1].bottom + margin
            pygame.draw.rect(self.screen, (255, 255, 255), (left, top, right - left, bottom - top), width=3, border_radius=15)



        # Vẽ mũi tên trái
        pygame.draw.polygon(self.screen, (255, 255, 255), [
            (self.arrow_left.right, self.arrow_left.top),
            (self.arrow_left.left, self.arrow_left.centery),
            (self.arrow_left.right, self.arrow_left.bottom)
        ])

        # Vẽ mũi tên phải
        pygame.draw.polygon(self.screen, (255, 255, 255), [
            (self.arrow_right.left, self.arrow_right.top),
            (self.arrow_right.right, self.arrow_right.centery),
            (self.arrow_right.left, self.arrow_right.bottom)
        ])

        for i, level in enumerate(self.levels):
            rect = self.buttons[i]
            is_hover = rect.collidepoint(mouse_pos)

            if level["unlocked"]:
                color = (80, 220, 80) if not is_hover else (120, 255, 120)
                pygame.draw.rect(self.screen, color, rect, border_radius=10)
                text = self.font.render(str(level["id"]), True, (0, 0, 0))
                self.screen.blit(text, text.get_rect(center=rect.center))
            else:
                # Vẽ hình ổ khóa thay vì màu xám
                lock_scaled = pygame.transform.smoothscale(self.lock_image, (rect.width, rect.height))
                self.screen.blit(lock_scaled, rect)

        # Vẽ chữ "MENU" ở giữa
        self.draw_title()

        # Vẽ nút Setting lên góc
        self.settings_button.draw()



        # # Khung bao quanh nút
        # if self.buttons:
        #     container_margin = 20
        #     left = self.buttons[0].left - container_margin
        #     top = self.buttons[0].top - container_margin
        #     right = self.buttons[1].right + container_margin
        #     bottom = self.buttons[2].bottom + container_margin
        #     pygame.draw.rect(self.screen, (255, 255, 255), (left, top, right - left, bottom - top), width=3, border_radius=15)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    result = self.settings_button.handle_event(event)
                    if result == "home":
                        return "menu"
                    # Chỉ xử lý các nút menu nếu popup setting đang đóng
                    if not self.settings_button.settings_menu_open:
                        if self.arrow_left.collidepoint(event.pos):
                            return "background"


                    elif self.arrow_right.collidepoint(event.pos):
                        print("→ Tiếp trang (chưa xử lý logic)")

                    for i, rect in enumerate(self.buttons):
                        if rect.collidepoint(event.pos):
                            if self.levels[i]["unlocked"]:
                                print(f"Bắt đầu màn {self.levels[i]['id']}")
                            else:
                                print("Màn này chưa mở!")
                
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.update_layout()
                    self.update_font_size()
                    self.settings_button.update_position(self.screen)


            self.draw()
            pygame.display.flip()
            clock.tick(60)

