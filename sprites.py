# Sprite classes
import pygame as pg
from settings import *
import random

vec = pg.math.Vector2


# noinspection PyArgumentList
class Player(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.walking = False
        self.jumping = False
        self.standing_frames = []
        self.walk_frames_r = []
        self.walk_frames_l = []
        self.jump_frame = []
        self.load_images()
        self.current_frame = 0  # to keep track of animation frame
        self.last_update = 0  # to keep time of animation
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        """アニメーションのフレーム画像をロード"""

        # 立っているときのフレーム
        self.standing_frames = [
            self.game.spritesheet.get_image(614, 1063, 120, 191),
            self.game.spritesheet.get_image(690, 406, 120, 201),
        ]
        # 個々のフレーム画像の背景を消す
        for frame in self.standing_frames:
            frame.set_colorkey((0, 0, 0))

        # 右を向いて歩いているときのフレーム
        self.walk_frames_r = [
            self.game.spritesheet.get_image(678, 860, 120, 201),
            self.game.spritesheet.get_image(692, 1458, 120, 207),
        ]
        # 個々のフレーム画像の背景を消す
        for frame in self.walk_frames_r:
            frame.set_colorkey((0, 0, 0))

        # 左を向いて歩いているときのフレーム
        self.walk_frames_l = []

        # 個々のフレーム画像の背景を消す
        for frame in self.walk_frames_r:
            frame.set_colorkey((0, 0, 0))
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))

        # jumpしているときのフレーム
        self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey((0, 0, 0))

    def jump(self):
        # jump only if on a platform
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.animate()
        # 重力の設定
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # 摩擦を計算
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # Velocity に Accelerationを足す
        self.vel += self.acc

        # 微かな動きを止める
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        # Position に Velocity を足す
        self.pos += self.vel + 0.5 * self.acc

        # Check Edges
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        # 現在の位置に Positionを設定
        self.rect.midbottom = self.pos

    def animate(self):
        """アニメーション"""
        now = pg.time.get_ticks()  # 現在のtick(時間)を取得
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        # 歩くアニメーション
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(
                    self.walk_frames_l)  # フレーム画像の配列番号を計算
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # アイドルアニメーション
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:  # 現在と最後にupdateした時間を比較
                self.last_update = now  # もしそうだったらlast_updateをnow(現在)に設定
                self.current_frame = (self.current_frame + 1) % len(
                    self.standing_frames)  # フレーム画像の配列番号を計算
                bottom = self.rect.bottom  # フレームごとにimageのサイズが変更になるかもしれないから
                # 地面に必ず足がついているように画像が変更になる前のbottom を取得
                self.image = self.standing_frames[
                    self.current_frame]  # imageを計算したフレームに画像に変更
                self.rect = self.image.get_rect()  # rectを新たに取得
                self.rect.bottom = bottom  # rectのbottomを更新


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        # spritesheetから地面の画像を２つ取得
        images = [self.game.spritesheet.get_image(0, 288, 380, 94),
                  self.game.spritesheet.get_image(213, 1662, 201, 100)]
        self.image = random.choice(images)  # 2つのうち１つをランダムに取得
        self.image.set_colorkey((0, 0, 0))  # 背景を消す
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
