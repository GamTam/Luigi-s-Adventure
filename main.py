import pickle
import pygame as pg
from Scripts.sprites import *
from Scripts.settings import *

pg.display.set_caption(title)
pg.mixer.pre_init(44100, -16, 2)
pg.init()

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()
        self.playerFriction = maxFriction
        self.hasPlayedIceSound = False
        self.pause = False
        self.pauseSound = False
        self.running = True
        self.going = False
        self.song_playing = ""
        self.font = pg.font.match_font(font)
        self.platWidth = width / 2
        self.loadData()

    def loadSounds(self):
        self.click = pg.mixer.Sound("sounds/click.ogg")
        self.jumpSound = pg.mixer.Sound("sounds/jomp.ogg")
        self.hopSound = pg.mixer.Sound("sounds/hop.ogg")
        self.gameStartSound = pg.mixer.Sound("sounds/okidoki.ogg")
        self.gameOverSound = pg.mixer.Sound("sounds/mamamia.ogg")
        self.iceSound = pg.mixer.Sound("sounds/aaaaa.ogg")
        self.hitSound = pg.mixer.Sound("sounds/waa!.ogg")
        self.crouchSound = pg.mixer.Sound("sounds/help.ogg")
        self.mushroomSound = pg.mixer.Sound("sounds/mushroom.ogg")
        self.enemyDieSound = pg.mixer.Sound("sounds/enemy_die.ogg")
        self.coinSound = pg.mixer.Sound("sounds/coin.ogg")

    def playSong(self, intro, song):
        if self.pause:
            # if self.pauseSound:
            #     self.click.play()
            #     self.pauseSound = False
            pg.mixer.pause()
            pg.mixer.music.pause()
        else:
            # if self.pauseSound:
            #     self.click.play()
            #     self.pauseSound = True
            pg.mixer.music.unpause()
            pg.mixer.unpause()

        if intro and not self.pause:
            if self.song_playing != "loop":
                if not pg.mixer.music.get_busy() and self.song_playing == "":
                    if self.song_playing == "":
                        pg.mixer.music.load("music/" + str(song) + "_intro.ogg")
                        self.song_playing = "intro"
                        pg.mixer.music.play()
                elif pg.mixer.music.get_pos() == -1:
                    pg.mixer.music.load("music/" + str(song) + "_main.ogg")
                    pg.mixer.music.play(-1)
                    self.song_playing = "loop"
        else:
            if self.song_playing != "loop":
                if  pg.mixer.music.get_pos() == -1:
                    pg.mixer.music.load("music/" + str(song) + ".ogg")
                    pg.mixer.music.play(-1)
                    self.song_playing = "loop"

        self.soundPos = pg.mixer.music.get_pos()
        self.totalLength = 15

    def NEWplaySong(self, introLength, loopLength, song):

        if self.pause:
            if self.pauseSound:
                self.click.play()
                self.pauseSound = False
            pg.mixer.music.pause()
        else:
            if self.pauseSound:
                self.click.play()
                self.pauseSound = False
            pg.mixer.music.unpause()

        if self.song_playing != "playing":
            pg.mixer.music.load("music/" + song + ".ogg")
            pg.mixer.music.play()
            self.song_playing = "playing"

        self.totalLength = introLength + loopLength
        self.soundPos = pg.mixer.music.get_pos() / 1000

        if self.soundPos >= self.totalLength and self.firstLoop:
            pg.mixer.music.play(0, self.soundPos - loopLength)
            self.firstLoop = False
            print("YEEEEEEEEE")
        elif self.soundPos >= loopLength and not self.firstLoop:
            pg.mixer.music.play(0, self.soundPos + introLength - loopLength)
            print("YOOOOOOOOO")


    def loadData(self):
        try:
            with open(saveFile, 'rb') as file:
                self.bestTime = pickle.load(file)
                self.bestDisplayTime = pickle.load(file)
                self.mostKills = pickle.load(file)
        except:
            self.bestTime = 0
            self.bestDisplayTime = "0:00"
            self.mostKills = 0

        self.pauseBackground = pg.image.load("sprites/pause.png").convert_alpha()
        self.loadSounds()

    def saveGame(self):
        with open(saveFile, 'wb') as file:
            pickle.dump(self.bestTime, file)
            pickle.dump(self.bestDisplayTime, file)
            pickle.dump(self.mostKills, file)

    def new(self):
        # restarts game
        self.loadData()
        self.jumpOffEnemy = 100
        self.mobSpawnRate = mobSpawnRate
        self.firstLoop = True
        self.gameStartSound.play()
        self.dieSound = False
        self.mobTimer = 0
        self.playtime = 0
        self.playSeconds = 0
        self.playMinutes = 0
        self.playHours = 0
        self.kills = 0
        self.score = 0
        self.platWidth = width / 2
        self.sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.fawfulcopters = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.particles = pg.sprite.Group()
        self.platformSpeed = 3
        self.player = Player(self)
        for plat in platformList:
            p = Platform(*plat)
            self.sprites.add(p)
            self.platforms.add(p)
        self.sprites.add(self.player)
        self.going = False
        self.touching = False
        self.pause = False
        self.run()

    def run(self):
        # Game Lööp
        self.playing = True

        while self.playing:
            # self.NEWplaySong(6.443, 53.348, "count bleck")
            # self.NEWplaySong(12.556, 62.233, "sammer's kingdom")
            # self.NEWplaySong(16.025, 70.378, "dimentio")
            self.NEWplaySong(9.007, 62.0, "champion of destruction")
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()
            pg.event.pump()

        pg.mixer.stop()
        self.gameOverSound.play()
        pg.mixer.music.stop()
        self.song_playing = ""

        self.playing = False

    def update(self):
        # Game Lööp - Update

        random.seed()

        if not self.pause:
            self.sprites.update()

            now = pg.time.get_ticks()
            if now - self.mobTimer > self.mobSpawnRate + random.choice([-1000, -500, 0, 500, 1000]):
                self.mobTimer = now
                Fawfulcopter(self)

            powerupHits = pg.sprite.spritecollide(self.player, self.powerups, False)
            if powerupHits:
                if powerupHits[0].type == "Mushroom":
                    self.mushroomSound.play()
                    self.player.health += 1
                    powerupHits[0].kill()
                elif powerupHits[0].type == "1UP":
                    self.mushroomSound.play()
                    self.player.health += 5
                    powerupHits[0].kill()

            mobHits = pg.sprite.spritecollide(self.player, self.fawfulcopters, False, pg.sprite.collide_mask)
            if mobHits:
                if mobHits[0].rect.y > 0 and mobHits[0].rect.x > 0 and mobHits[0].rect.x < width:
                    if self.player.rect.bottom - 50 < mobHits[0].rect.top and not self.player.dead and not mobHits[0].dead:
                        mobHits[0].sound.stop()
                        mobHits[0].dead = True
                        self.enemyDieSound.play()
                        self.kills += 1
                        enemyCoin(mobHits[0].rect.x, mobHits[0].rect.y, self)
                        self.player.vel.y = 0
                        self.player.vel.y -= jumpPower / 3
                        self.jumpOffEnemy = 0
                        self.player.jumping = False
                    elif not self.player.dead and not mobHits[0].dead:
                        self.player.dead = True
                        if not self.dieSound:
                            self.hitSound.play()
                            self.player.health -= 1
                            self.dieSound = True

            if self.jumpOffEnemy < 10:
                self.jumpOffEnemy += 1

            if self.player.vel.y > 0:
                hits = pg.sprite.spritecollide(self.player, self.platforms, False)
                if hits:
                    if not self.going:
                        if self.player.pos.y < hits[0].rect.bottom:
                            self.player.pos.y = hits[0].rect.top + 1
                            self.player.vel.y = 0
                            self.player.jumping = False
                            self.jumpOffEnemy = 100
                    else:
                        if self.player.pos.y < hits[0].rect.bottom:
                            self.player.pos.y = hits[0].rect.top + self.platformSpeed
                            self.player.vel.y = 0
                            self.player.jumping = False
                            self.jumpOffEnemy = 100

                    if hits[0].color == 1:
                        self.playerFriction = minFriction
                    else:
                        self.playerFriction = maxFriction


            if self.score == 25:
                if self.mobSpawnRate > 1000:
                    self.mobSpawnRate -= 500
                self.score = 0

            if self.player.rect.top <= height / 4:
                self.going = True
            #     self.player.pos.y += abs(self.player.vel.y)

            if self.going:
                for fawfulcopter in self.fawfulcopters:
                    fawfulcopter.rect.y += self.platformSpeed
                    if fawfulcopter.rect.top > height:
                        fawfulcopter.sound.stop()
                        fawfulcopter.kill()
                for plat in self.platforms:
                    # plat.rect.y += abs(self.player.vel.y)
                    plat.rect.y += self.platformSpeed
                    if plat.rect.top > height:
                        plat.kill()
                        self.score += 1
                        if self.platWidth != 150:
                            self.platWidth -= 1
                for pow in self.powerups:
                    pow.rect.y += self.platformSpeed
                    if pow.rect.top > height:
                        pow.kill()

            if len(self.platforms) < 3:
                x = random.randrange(0, width - self.platWidth)
                w = random.randrange(1, 6)
                spawn = random.randrange(0, 5000)
                p = Platform(x, -64, random.randrange(0, 10), w)
                if spawn < 100:
                    if w > 3:
                        Mushroom(x + random.randrange(32, 160), -64, self)
                    else:
                        Mushroom(x + random.randrange(32, 288), -64, self)
                if spawn == 7:
                    if w > 3:
                        oneUP(x + random.randrange(32, 160), -64, self)
                    else:
                        oneUP(x + random.randrange(32, 288), -64, self)

                self.platforms.add(p)
                self.sprites.add(p)

            if self.player.rect.top > height:
                self.player.kill()
                for sprite in self.sprites:
                    sprite.rect.y -= 40
                    if sprite.rect.bottom < 0:
                        sprite.kill()
                if len(self.platforms) == 0:
                    self.playing = False

            if not self.player.dead:
                if self.going:
                    self.playtime += 1

                self.playSeconds = self.playtime // fps
                self.playMinutes = self.playSeconds // 60
                self.playHours = self.playMinutes // 60

                if self.playSeconds >= 60:
                    self.playSeconds %= 60
                if self.playSeconds < 10 and self.playMinutes >= 1:
                    self.playSeconds = "0{0}".format(self.playSeconds)

                if self.playMinutes >= 60:
                    self.playMinutes %= 60
                if self.playMinutes == 0:
                    self.playMinutes = ""
                elif self.playMinutes < 10 and self.playHours >= 1:
                    self.playMinutes = "0{0}:".format(self.playMinutes)
                else:
                    self.playMinutes = "{0}:".format(self.playMinutes)

                if self.playHours == 0:
                    self.playHours = ""
                else:
                    self.playHours = "{0}:".format(self.playHours)

                self.playSeconds = str(self.playSeconds)
                self.playMinutes = str(self.playMinutes)
                self.playHours = str(self.playHours)

                self.displayTime = self.playHours + self.playMinutes + self.playSeconds

                if self.going:
                    if self.playtime % fps == 0:
                        if bgColor[0] != 255 and bgColor[2] < 0:
                            bgColor[0] += 1
                        if bgColor[1] != 0:
                            bgColor[1] -= 1
                        if bgColor[2] != 0 and bgColor[1] < 0:
                            bgColor[2] -= 1
        else:
            for fawfulcopter in self.fawfulcopters:
                fawfulcopter.sound.stop()
                fawfulcopter.playingSound = False

    def events(self):
        # Game Lööp - Events
        for event in pg.event.get():
            self.keys = pg.key.get_pressed()
            # check for closing window
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_UP or event.key == pg.K_w:
                    if not self.pause:
                        if not self.player.dead:
                            self.player.jump()
                if event.key == pg.K_RETURN:
                    if self.pause:
                        self.pause = False
                        self.pauseSound = True
                    else:
                        self.pause = True
                        self.pauseSound = True

    def draw(self):
        # Game Lööp - Draw
        self.screen.fill(bgColor)
        self.sprites.draw(self.screen)
        self.platforms.draw(self.screen)
        self.powerups.draw(self.screen)
        self.fawfulcopters.draw(self.screen)
        self.particles.draw(self.screen)
        if self.pause:
            self.screen.blit(self.pauseBackground, (0,0))
        if self.player.health > 0:
            self.drawText("Time: " + self.displayTime, 22, white, width / 2, 15)
            self.drawText("Kills: " + str(self.kills), 22, white, width * (3/4), 15)
            self.drawText("Health: " + str(self.player.health), 22, white, width / 4, 15)
        else:
            self.drawText("Time: " + self.displayTime, 100, yellow, width / 2, height / 2 - 50)
        # DO THIS ONE LAST
        pg.display.flip()

    def drawText(self, text, size, color, x, y):
        fnt = pg.font.Font("fonts/" + font, size)
        textSurface = fnt.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.midtop = (int(x), int(y))
        self.screen.blit(textSurface, textRect)

    def splashScreen(self):
        self.playSong(False, 'title screen')
        self.screen.fill(bgColor)
        self.drawText(title, 40, white, width / 2, height / 4)
        self.drawText("If you want to keep your knees, press a button!", 20, white, width / 2, height * 3 / 4)
        self.drawText("The longest time is " + str(self.bestDisplayTime) + ", by the way", 20, white, width / 2, height * 3 / 4 + 50)
        pg.display.flip()
        self.waitForKey()
        pg.mixer.music.stop()
        self.song_playing = ""

    def gameOver(self):
        self.playSong(False, "game_over")
        if not self.running:
            return
        self.screen.fill(bgColor)
        self.drawText("YOU DIED!", 40, white, width / 2, height / 4)
        # self.drawText("Your score was: " + str(self.score), 20, white, width / 2, height / 2)
        self.drawText("Your time was: " + str(self.displayTime), 20, white, width / 2, height / 2)
        self.drawText("Your total kills: " + str(self.kills), 20, white, width / 2, height / 2 + 50)
        self.drawText("I hope you still like your knees.", 20, white, width / 2, height * 3 / 4)

        if self.playtime > self.bestTime:
            self.bestTime = self.playtime
            self.bestDisplayTime = self.displayTime
            self.drawText("That's your new best, BTW", 20, white, width / 2, height / 2 + 25)
            self.saveGame()
        else:
            self.drawText("The current best time is " + str(self.bestDisplayTime), 20, white, width / 2,
            height * 3 / 4 + 25)

        if self.kills > self.mostKills:
            self.mostKills = self.kills
            self.drawText("That's a lot of kills", 20, white, width / 2, height / 2 + 75)
            self.saveGame()
        else:
            self.drawText("The most kills you've had are " + str(self.mostKills), 20, white, width / 2,
                          height * 3 / 4 + 50)


        pg.display.flip()
        self.waitForKey()
        pg.mixer.stop()
        pg.mixer.music.stop()
        self.song_playing = ""

    def waitForKey(self):
        waiting = True
        while waiting:
            self.keys = pg.key.get_pressed()
            self.clock.tick(fps)
            for event in pg.event.get():
                self.keys = pg.key.get_pressed()
                if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

game = Game()
game.splashScreen()

while game.running:
    game.new()
    bgColor = list(lightBlue)
    game.gameOver()

pg.quit()
