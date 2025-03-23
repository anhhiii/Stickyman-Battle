import pygame
from utils import load_image

class Enemy:
    def __init__(self, type, hp, damage, speed, x, y):
        self.type = type
        self.hp = hp
        self.damage = damage
        self.speed = speed
        self.x = x
        self.y = y
        self.image = load_image(f"assets/sprites/{type}.png")

    def chase_player(self, player):
        """Quái di chuyển về phía người chơi"""
        if self.x < player.x:
            self.x += self.speed
        if self.x > player.x:
            self.x -= self.speed
        if self.y < player.y:
            self.y += self.speed
        if self.y > player.y:
            self.y -= self.speed
