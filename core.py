
import pygame
from svp_modules.game.gmod.gm import HGame

class DataCore:

    def __init__(self):
        self.health = 5
        self.posX = HGame.MidX
        self.posY = HGame.Height - 100

    def draw(self):
        pygame.draw.circle(HGame.Canvas, (0,255,255), (self.posX, self.posY), 30)

    def take_hit(self):
        self.health -= 1

    def is_destroyed(self):
        return self.health <= 0