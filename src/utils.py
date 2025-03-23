import pygame
import os

def load_image(path):
    """Load ảnh từ file và kiểm tra lỗi"""
    if isinstance(path, pygame.Surface):
        return path  # Nếu path là Surface rồi thì trả về luôn

    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    full_path = os.path.join(base_path, path)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Không tìm thấy file hình ảnh: {full_path}")

    return pygame.image.load(full_path).convert_alpha()

def load_sprite_sheet(sheet, frame_width, frame_height, num_frames):
    """Cắt ảnh sprite sheet thành từng frame nhỏ."""
    frames = []
    for i in range(num_frames):
        frame = sheet.subsurface(pygame.Rect(
            i * frame_width, 0, frame_width, frame_height
        ))
        frames.append(frame)
    return frames
