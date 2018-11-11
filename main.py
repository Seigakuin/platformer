import pygame as pg
import random
from settings import *
from sprites import *
from os import path


class SpriteSheet:
    def __init__(self, filename):
        """ SpriteSheet専用クラス"""
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        """ spritesheetの中の特定の画像を切り取る """
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image


class Game:
    def __init__(self):
        """ ゲームを初期化 """
        self.running = True
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.all_sprites = None
        self.platforms = None
        self.playing = False
        self.player = None
        self.score = 0
        self.highscore = 0
        self.dir = None
        self.spritesheet = None

        self.font_name = pg.font.match_font(FONT_NAME)  # FONTを探す
        self.load_data()

    def load_data(self):
        """ HighScoreデータをロード """
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # spritesheetをロード
        self.spritesheet = SpriteSheet(path.join(img_dir, SPRITESHEET))

    def new(self):
        # ゲームオーバー後のニューゲーム
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()

        self.player = Player(self)
        self.all_sprites.add(self.player)

        for plat in PLATFORM_LIST:
            p = Platform(self, *plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # ゲームループ
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # アップデート
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top + 1
                self.player.vel.y = 0

        # もしplayerが画面上部1/4に達したら
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)  # abs = 絶対値を取得
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                # 画面外に行ったplatformを消す
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10

        # ゲームオーバー
        # 落下を表現
        if self.player.rect.bottom > HEIGHT:
            # 全てのsprite
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)  # max値を取得
                if sprite.rect.bottom < 0:  # spriteが画面上部に消えたら
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # 新しいplatform を作成 / 画面には平均的に同じ数のplatform
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)

            p = Platform(self, random.randrange(0, WIDTH - width),
                         random.randrange(-75, -30))
            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        # イベント
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # 描画
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()

    def show_start_screen(self):
        # ゲームスタート画面
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2,
                       HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2,
                       HEIGHT * 3 / 4)
        self.draw_text("HIGH SCORE: {}".format(str(self.highscore)), 22, WHITE,
                       WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # ゲームオーバー画面
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: {}".format(str(self.score)), 22, WHITE,
                       WIDTH / 2,
                       HEIGHT / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2,
                       HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2,
                           HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
                print("finished writing")
        else:
            self.draw_text("HIGH SCORE: {}".format(str(self.highscore)), 22,
                           WHITE,
                           WIDTH / 2, HEIGHT / 2 + 40)

        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
