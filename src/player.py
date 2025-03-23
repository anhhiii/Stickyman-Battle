import pygame
from utils import load_image

class Player:
    
    def __init__(self, x, y, hp, weapon, image_path):
        self.x = x
        self.y = y
        self.hp = hp
        self.weapon = weapon
        self.image_path = image_path


    def move(self, keys):
        """Di chuyển người chơi"""
        if keys[pygame.K_LEFT]:
            self.x -= 5
        if keys[pygame.K_RIGHT]:
            self.x += 5
        if keys[pygame.K_UP]:
            self.y -= 5
        if keys[pygame.K_DOWN]:
            self.y += 5
