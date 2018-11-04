# Sprite classes
import pygame as pg
from settings import *

vec = pg.math.Vector2


# noinspection PyArgumentList
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.vx = 0
        self.vy = 0

    def update(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # 摩擦を計算
        self.acc += self.vel * PLAYER_FRICTION
        # Velocity に Accelerationを足す
        self.vel += self.acc
        # Position に Velocity を足す
        self.pos += self.vel + 0.5 * self.acc
        # 現在の位置に Positionを設定
        self.rect.center = self.pos
