import pygame as pg
import random
from settings import *


class Game:
    def __init__(self):
        # ゲームを初期化
        self.running = True

    def new(self):
        # ゲームオーバー後のニューゲーム
        pass

    def run(self):
        # ゲームループ
        pass

    def update(self):
        # アップデート
        pass

    def events(self):
        # イベント
        pass

    def draw(self):
        # 描画
        pass

    def show_start_screen(self):
        # ゲームスタート画面
        pass

    def show_go_screen(self):
        # ゲームオーバー画面
        pass


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
