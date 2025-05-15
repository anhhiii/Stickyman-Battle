import pygame
import sys
import os

class SettingsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

        # Thu nhỏ khung menu
        self.menu_rect = pygame.Rect(0, 0, 150, 300)  # width, height (giảm kích thước)
        self.menu_rect.center = (screen.get_width() // 2, screen.get_height() // 2)  # Căn giữa màn hình

        # Tải icon cho các nút
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))

        self.home_icon = pygame.image.load(os.path.join(project_root, 'assets', 'icons', 'home_icon.png'))
        self.home_icon = pygame.transform.scale(self.home_icon, (50, 50))  # Resize icon Home (nhỏ hơn)

        self.volume_icon_on = pygame.image.load(os.path.join(project_root, 'assets', 'icons', 'volume_icon.png'))
        self.volume_icon_on = pygame.transform.scale(self.volume_icon_on, (50, 50))  # Icon âm thanh bật

        self.volume_icon_off = pygame.image.load(os.path.join(project_root, 'assets', 'icons', 'mute_icon.png'))
        self.volume_icon_off = pygame.transform.scale(self.volume_icon_off, (50, 50))  # Icon âm thanh tắt

        self.back_icon = pygame.image.load(os.path.join(project_root, 'assets', 'icons', 'back_icon.png'))
        self.back_icon = pygame.transform.scale(self.back_icon, (50, 50))  # Resize icon Back (nhỏ hơn)

        # Căn chỉnh lại vị trí các nút
        self.home_button = self.home_icon.get_rect(center=(self.menu_rect.centerx, self.menu_rect.top + 70))
        self.volume_button = self.volume_icon_on.get_rect(center=(self.menu_rect.centerx, self.menu_rect.top + 150))
        self.back_button = self.back_icon.get_rect(center=(self.menu_rect.centerx, self.menu_rect.top + 230))

        # Trạng thái âm thanh (bật mặc định)
        self.sound_on = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.home_button.collidepoint(event.pos):
                        return "menu"  # Quay lại menu chính
                    elif self.volume_button.collidepoint(event.pos):
                        self.toggle_sound()  # Bật/tắt âm thanh
                    elif self.back_button.collidepoint(event.pos):
                        return "back"  # Quay lại màn chơi

            # Vẽ menu cài đặt
            self.draw_menu()

            pygame.display.flip()

    def toggle_sound(self):
        """Bật hoặc tắt âm thanh và cập nhật trạng thái nhạc nền."""
        self.sound_on = not self.sound_on
        if self.sound_on:
            pygame.mixer.music.unpause()  # Bật nhạc nền
        else:
            pygame.mixer.music.pause()  # Tắt nhạc nền

    def draw_menu(self):
        # Vẽ khung menu (bo góc và có viền)
        pygame.draw.rect(self.screen, (0, 0, 0), self.menu_rect, border_radius=15)  # Viền đen
        pygame.draw.rect(self.screen, (255, 255, 200), self.menu_rect.inflate(-8, -8), border_radius=15)  # Menu màu vàng nhạt

        # Vẽ icon Home
        self.screen.blit(self.home_icon, self.home_button.topleft)

        # Vẽ icon Volume (hiển thị icon phù hợp với trạng thái âm thanh)
        if self.sound_on:
            self.screen.blit(self.volume_icon_on, self.volume_button.topleft)
        else:
            self.screen.blit(self.volume_icon_off, self.volume_button.topleft)

        # Vẽ icon Back
        self.screen.blit(self.back_icon, self.back_button.topleft)



