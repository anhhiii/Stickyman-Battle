import pygame
from utils import load_image

def game_loop(screen, level):
    running = True
    clock = pygame.time.Clock()

    # Load ảnh người chơi và quái
    player_sprite = load_image(level.player.image_path)

    enemy_sprites = [load_image(enemy.image) for enemy in level.enemies]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Xử lý khi resize cửa sổ
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        # Cập nhật nền theo kích thước mới
        background = pygame.transform.scale(
            load_image(level.background),
            (screen.get_width(), screen.get_height())
        )

        # Vẽ nền
        screen.blit(background, (0, 0))

        # Tính lại kích thước nhân vật theo tỉ lệ màn hình mới
        player_scaled = pygame.transform.scale(
            player_sprite,
            (int(player_sprite.get_width() * (screen.get_width() / 1280)),
             int(player_sprite.get_height() * (screen.get_height() / 720)))
        )

        # Vẽ người chơi
        screen.blit(player_scaled, (level.player.x, level.player.y))

        # Vẽ từng quái vật (scale theo tỉ lệ)
        for i, enemy in enumerate(level.enemies):
            enemy_scaled = pygame.transform.scale(
                enemy_sprites[i],
                (int(enemy_sprites[i].get_width() * (screen.get_width() / 1280)),
                 int(enemy_sprites[i].get_height() * (screen.get_height() / 720)))
            )
            screen.blit(enemy_scaled, (enemy.x, enemy.y))

        # Cập nhật màn hình
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
