"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (35, 45, 35)
COLOR_PLAYER = (80, 180, 255)
COLOR_OBSTACLE = (220, 60, 60)
COLOR_OBSTACLE_BORDER = (120, 20, 20)
COLOR_TEXT = (255, 255, 255)

_big_font = None


def draw_scene(surface, player, coins, obstacles=(), hide_player=False):
    surface.fill(COLOR_BG)
    for coin in coins:
        pygame.draw.circle(surface, coin.color, (int(coin.x), int(coin.y)), coin.radius)
    for obstacle in obstacles:
        rect = obstacle.get_rect()
        pygame.draw.rect(surface, COLOR_OBSTACLE, rect)
        pygame.draw.rect(surface, COLOR_OBSTACLE_BORDER, rect, width=3)
    if not hide_player:
        pygame.draw.rect(surface, COLOR_PLAYER, player.get_rect(), border_radius=4)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)


def draw_game_over(surface, font, score, reason):
    """Dark overlay with Game Over, the reason, final score, and restart hint."""
    global _big_font
    if _big_font is None:
        _big_font = pygame.font.SysFont("consolas", 52, bold=True)

    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    surface.blit(overlay, (0, 0))

    cx = surface.get_width() // 2
    cy = surface.get_height() // 2

    lines = [
        (_big_font, "GAME OVER", (255, 90, 90), cy - 80),
        (font, reason, (220, 220, 220), cy - 25),
        (_big_font, f"Final Score: {score}", (255, 220, 80), cy + 25),
        (font, "Press R to play again", (255, 255, 255), cy + 90),
    ]
    for fnt, text, color, y in lines:
        surf = fnt.render(text, True, color)
        surface.blit(surf, surf.get_rect(center=(cx, y)))