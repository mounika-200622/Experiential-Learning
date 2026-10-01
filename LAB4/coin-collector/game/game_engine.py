"""
GameEngine: owns the player, coins, obstacles, and round state.

Task 1: collected coins are removed, so each is collected exactly once.
Task 2: three coin types (bronze, silver, gold).
Task 3: obstacles cost a life, with a short invincibility window.
Task 4: 30-second round; ends on time up or 0 lives; press R to restart.
"""

import math
import random
import pygame

from game.player import Player
from game.coin import Coin
from game.obstacle import Obstacle
from game.collection import check_collection
from game.renderer import WIDTH, HEIGHT

FPS = 60
NUM_COINS = 6
NUM_OBSTACLES = 4
START_LIVES = 3
INVINCIBLE_FRAMES = 90  # 1.5 seconds at 60 FPS
ROUND_SECONDS = 30

# (name, value, color, spawn weight) - higher weight = more common
COIN_TYPES = [
    ("bronze", 1, (205, 127, 50), 60),
    ("silver", 3, (192, 192, 192), 30),
    ("gold", 5, (255, 215, 0), 10),
]


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        """Start a fresh round: score, lives, timer, coins, obstacles."""
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
        self.coins = [self._random_coin() for _ in range(NUM_COINS)]
        self.obstacles = self._spawn_obstacles()
        self.score = 0
        self.lives = START_LIVES
        self.invincible_frames = 0
        self.frames_left = ROUND_SECONDS * FPS
        self.game_over = False
        self.game_over_reason = ""

    def _random_coin(self):
        x = random.randint(30, WIDTH - 30)
        y = random.randint(30, HEIGHT - 30)
        weights = [t[3] for t in COIN_TYPES]
        _, value, color, _ = random.choices(COIN_TYPES, weights=weights, k=1)[0]
        return Coin(x=x, y=y, radius=12, value=value, color=color)

    def _spawn_obstacles(self):
        """Place obstacles inside the play area, away from the player,
        the coins, and each other."""
        obstacles = []
        safe_zone = self.player.get_rect().inflate(160, 160)
        attempts = 0
        while len(obstacles) < NUM_OBSTACLES and attempts < 500:
            attempts += 1
            size = 34
            margin = size // 2 + 5
            x = random.randint(margin, WIDTH - margin)
            y = random.randint(margin, HEIGHT - margin)
            candidate = Obstacle(x, y, size)
            rect = candidate.get_rect()
            if rect.colliderect(safe_zone):
                continue
            if any(rect.colliderect(c.get_rect().inflate(10, 10)) for c in self.coins):
                continue
            if any(rect.colliderect(o.get_rect().inflate(20, 20)) for o in obstacles):
                continue
            obstacles.append(candidate)
        return obstacles

    def handle_event(self, event):
        """Press R after the round ends to start a new one."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.game_over:
            self.reset()

    def handle_input(self, keys_pressed):
        if self.game_over:
            return
        dx = dy = 0
        if keys_pressed[pygame.K_UP]:
            dy -= self.player.speed
        if keys_pressed[pygame.K_DOWN]:
            dy += self.player.speed
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.player.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.player.speed
        self.player.move(dx, dy, WIDTH, HEIGHT)

    def update(self):
        if self.game_over:
            return

        # Coins (Task 1 + 2)
        collected = check_collection(self.player, self.coins)
        for coin in collected:
            self.score += coin.value
            self.coins.remove(coin)

        # Invincibility countdown
        if self.invincible_frames > 0:
            self.invincible_frames -= 1

        # Obstacles (Task 3): lose one life per hit, then become invincible
        if self.invincible_frames == 0:
            player_rect = self.player.get_rect()
            for obstacle in self.obstacles:
                if player_rect.colliderect(obstacle.get_rect()):
                    self.lives -= 1
                    self.invincible_frames = INVINCIBLE_FRAMES
                    break

        # Timer (Task 4)
        self.frames_left -= 1

        # Round end: lives out or time up, whichever comes first
        if self.lives <= 0:
            self.game_over = True
            self.game_over_reason = "You ran out of lives!"
        elif self.frames_left <= 0:
            self.frames_left = 0
            self.game_over = True
            self.game_over_reason = "Time's up!"

    def draw(self, surface, font):
        from game import renderer
        # Blink the player while invincible
        blink_hidden = (
            self.invincible_frames > 0
            and not self.game_over
            and (pygame.time.get_ticks() // 100) % 2 == 0
        )
        renderer.draw_scene(
            surface, self.player, self.coins, self.obstacles, hide_player=blink_hidden
        )
        seconds_left = math.ceil(self.frames_left / FPS)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 40))
        renderer.draw_text(surface, font, f"Time: {seconds_left}", (WIDTH - 130, 10))

        if self.game_over:
            renderer.draw_game_over(surface, font, self.score, self.game_over_reason)