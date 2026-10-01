"""
Obstacle: a static hazard square. Touching it costs the player a life.
"""

import pygame


class Obstacle:
    def __init__(self, x, y, size=34):
        self.x = x
        self.y = y
        self.size = size

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.size / 2), int(self.y - self.size / 2),
            self.size, self.size,
        )