import pygame as pg
import xml.etree.ElementTree as ET
from Scripts.settings import *

vec = pg.math.Vector2


class spritesheet:
    def __init__(self, img_file, data_file=None):
        self.spritesheet = pg.image.load(img_file).convert_alpha()
        if data_file:
            tree = ET.parse(data_file)
            self.map = {}
            for node in tree.iter():
                if node.attrib.get('n'):
                    name = node.attrib.get('n')
                    self.map[name] = {}
                    self.map[name]['x'] = int(node.attrib.get('x'))
                    self.map[name]['y'] = int(node.attrib.get('y'))
                    self.map[name]['width'] = int(node.attrib.get('w'))
                    self.map[name]['height'] = int(node.attrib.get('h'))

    def get_image_rect(self, x, y, w, h):
        return self.spritesheet.subsurface(pg.Rect(x, y, w, h))

    def getImageName(self, name):
        rect = pg.Rect(self.map[name]['x'], self.map[name]['y'], self.map[name]['width'], self.map[name]['height'])
        return self.spritesheet.subsurface(rect)


class Luigi(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.health = 3
        self.deadTimer = 0
        self.dead = False
        self.walking = False
        self.jumping = False
        self.playIceSound = True
        self.playCrouchSound = True
        self.crouching = False
        self.currentFrame = 0
        self.lastUpdate = 0
        self.crouchTimer = 0
        self.loadImages()
        self.facing = 'Right'
        self.hit = False
        self.image = self.standingFrame[0]
        self.currentJumpFrame = 0
        self.currentFrame = 0
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        self.pos = vec(width / 2 - 50, height / 2 + 25)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.mask = pg.mask.from_surface(self.image)

    def loadImages(self):
        sheet = spritesheet("sprites/loogi.png", "sprites/loogi.xml")

        self.standingFrame = [sheet.getImageName("luigi_standing.png"),
                              pg.transform.flip(sheet.getImageName("luigi_standing.png"), True, False)]

        self.walkingFramesRight = [sheet.getImageName("luigi_running_1.png"),
                                   sheet.getImageName("luigi_running_2.png"),
                                   sheet.getImageName("luigi_running_3.png"),
                                   sheet.getImageName("luigi_running_4.png"),
                                   sheet.getImageName("luigi_running_5.png"),
                                   sheet.getImageName("luigi_running_6.png"),
                                   sheet.getImageName("luigi_running_7.png"),
                                   sheet.getImageName("luigi_running_8.png"),
                                   sheet.getImageName("luigi_running_9.png"),
                                   sheet.getImageName("luigi_running_10.png"),
                                   sheet.getImageName("luigi_running_11.png"),
                                   sheet.getImageName("luigi_running_12.png")]
        self.walkingFramesLeft = []
        for frame in self.walkingFramesRight:
            self.walkingFramesLeft.append(pg.transform.flip(frame, True, False))

        self.jumpingFramesRight = [sheet.getImageName("luigi_jumping.png")]

        self.jumpingFramesLeft = []
        for frame in self.jumpingFramesRight:
            self.jumpingFramesLeft.append(pg.transform.flip(frame, True, False))

        self.iceFramesRight = [sheet.getImageName("luigi_scared_1.png"),
                               sheet.getImageName("luigi_scared_2.png"),
                               sheet.getImageName("luigi_scared_3.png"),
                               sheet.getImageName("luigi_scared_4.png"),
                               sheet.getImageName("luigi_scared_5.png"),
                               sheet.getImageName("luigi_scared_6.png")]

        self.iceFramesLeft = []
        for frame in self.iceFramesRight:
            self.iceFramesLeft.append(pg.transform.flip(frame, True, False))

        self.deadFrames = sheet.getImageName("luigi_dead.png")

        self.crouchingFramesRight = [sheet.getImageName("luigi_crouch_1.png"),
                                     sheet.getImageName("luigi_crouch_2.png"),
                                     sheet.getImageName("luigi_crouch_3.png"),
                                     sheet.getImageName("luigi_crouch_4.png"),
                                     sheet.getImageName("luigi_crouch_5.png"),
                                     sheet.getImageName("luigi_crouch_6.png"),
                                     sheet.getImageName("luigi_crouch_7.png"),
                                     sheet.getImageName("luigi_crouch_8.png"),
                                     sheet.getImageName("luigi_crouch_9.png"),
                                     sheet.getImageName("luigi_crouch_10.png"),
                                     sheet.getImageName("luigi_crouch_11.png"),
                                     sheet.getImageName("luigi_crouch_12.png"),
                                     sheet.getImageName("luigi_crouch_13.png"),
                                     sheet.getImageName("luigi_crouch_14.png"),
                                     sheet.getImageName("luigi_crouch_15.png"),
                                     sheet.getImageName("luigi_crouch_16.png"),
                                     sheet.getImageName("luigi_crouch_17.png"),
                                     sheet.getImageName("luigi_crouch_18.png"),
                                     sheet.getImageName("luigi_crouch_19.png"),
                                     sheet.getImageName("luigi_crouch_20.png"),
                                     sheet.getImageName("luigi_crouch_21.png"),
                                     sheet.getImageName("luigi_crouch_22.png"),
                                     sheet.getImageName("luigi_crouch_23.png"),
                                     sheet.getImageName("luigi_crouch_24.png"),
                                     sheet.getImageName("luigi_crouch_25.png"),
                                     sheet.getImageName("luigi_crouch_26.png"),
                                     sheet.getImageName("luigi_crouch_27.png"),
                                     sheet.getImageName("luigi_crouch_28.png"),
                                     sheet.getImageName("luigi_crouch_29.png"),
                                     sheet.getImageName("luigi_crouch_30.png"),
                                     sheet.getImageName("luigi_crouch_31.png"),
                                     sheet.getImageName("luigi_crouch_32.png"),
                                     sheet.getImageName("luigi_crouch_33.png"),
                                     sheet.getImageName("luigi_crouch_34.png"),
                                     sheet.getImageName("luigi_crouch_35.png"),
                                     sheet.getImageName("luigi_crouch_36.png")]

        self.crouchingFramesLeft = []
        for frame in self.crouchingFramesRight:
            self.crouchingFramesLeft.append(pg.transform.flip(frame, True, False))

    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            if not self.jumping and not self.crouching:
                self.vel.y -= jumpPower

                self.game.jumpSound.play()
                self.jumping = True
            if not self.jumping and self.crouching:
                self.vel.y -= jumpPower / 2

                self.game.hopSound.play()

        if self.game.jumpOffEnemy < 10:
            if not self.jumping and not self.crouching:
                self.vel.y -= (jumpPower / 2)

                self.game.jumpSound.play()
                self.jumping = True
                self.game.jumpOffEnemy = 100

    def update(self):
        self.animate()
        self.acc = vec(0, playerGrav)
        keys = pg.key.get_pressed()
        if not self.hit:

            if not self.jumping and (keys[pg.K_s]):
                self.crouching = True
            else:
                self.crouching = False

            if keys[pg.K_a] and not self.crouching:
                if not self.crouching:
                    self.acc.x = -playerAcc
                    self.facing = "Left"
                    if keys[pg.K_LSHIFT]:
                        self.acc.x = playerAcc * -2
            if keys[pg.K_d] and not self.crouching:
                if not self.crouching:
                    self.acc.x = playerAcc
                    self.facing = "Right"
                    if keys[pg.K_LSHIFT]:
                        self.acc.x = playerAcc * 2

        self.acc.x += self.vel.x * self.game.playerFriction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if self.pos.x > width + 15:
            self.pos.x = -15
        if self.pos.x < -15:
            self.pos.x = width + 15
        self.rect.midbottom = self.pos
        if self.game.going:
            self.rect.y += self.game.platformSpeed

        self.crouchTimer += 1

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0 and not self.crouching:
            self.walking = True
        else:
            self.walking = False

        if self.hit and self.deadTimer < fps:
            self.image = self.deadFrames
            self.deadTimer += 1
            self.rect = self.image.get_rect()
        elif self.hit and self.deadTimer == fps and self.health > 0:
            self.jumping = True
            pg.mixer.Sound.play(self.game.hopSound)
            self.vel.y -= jumpPower / 3
            self.game.dieSound = False
            self.hit = False
            self.deadTimer = 0

        if not self.hit:
            if self.crouching:
                if now - self.lastUpdate > 50:
                    self.lastUpdate = now
                    if self.currentFrame < len(self.crouchingFramesRight):
                        self.currentFrame = (self.currentFrame + 1) % (len(self.crouchingFramesRight))
                    else:
                        self.currentFrame = 0
                    bottom = self.rect.bottom
                    if self.facing == "Right":
                        self.image = self.crouchingFramesRight[self.currentFrame]
                        if self.playCrouchSound:
                            self.game.crouchSound.play()
                            self.playCrouchSound = False
                    elif self.facing == "Left":
                        self.image = self.crouchingFramesLeft[self.currentFrame]
                        if self.playCrouchSound:
                            self.game.crouchSound.play()
                            self.playCrouchSound = False
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom

            if self.jumping or self.game.jumpOffEnemy < 10:
                self.playCrouchSound = True
                if now - self.lastUpdate > 100:
                    self.lastUpdate = now
                    if self.currentJumpFrame < len(self.jumpingFramesRight) - 1:
                        self.currentJumpFrame = (self.currentJumpFrame + 1)
                    bottom = self.rect.bottom
                    if self.facing == "Right":
                        self.image = self.jumpingFramesRight[self.currentJumpFrame]
                    elif self.facing == 'Left':
                        self.image = self.jumpingFramesLeft[self.currentJumpFrame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom

            elif self.walking:
                self.currentJumpFrame = 0
                self.playCrouchSound = True
                if self.game.playerFriction == -0.07:
                    if now - self.lastUpdate > 50:
                        self.lastUpdate = now
                        self.currentFrame = (self.currentFrame + 1) % len(self.walkingFramesRight)
                        bottom = self.rect.bottom
                        if self.vel.x > 0:
                            self.image = self.walkingFramesRight[self.currentFrame]
                            self.playIceSound = True
                        else:
                            self.image = self.walkingFramesLeft[self.currentFrame]
                            self.playIceSound = True
                        self.rect = self.image.get_rect()
                        self.rect.bottom = bottom
                    if abs(self.vel.x) < 0.7:
                        self.vel.x = 0

                else:
                    if now - self.lastUpdate > 40:
                        self.lastUpdate = now
                        self.currentFrame = (self.currentFrame + 1) % len(self.iceFramesRight)
                        bottom = self.rect.bottom
                        if self.vel.x > 0:
                            self.image = self.iceFramesRight[self.currentFrame]
                            if self.playIceSound:
                                self.game.iceSound.play()
                                self.playIceSound = False
                        else:
                            self.image = self.iceFramesLeft[self.currentFrame]
                            if self.playIceSound:
                                self.game.iceSound.play()
                                self.playIceSound = False
                        self.rect = self.image.get_rect()
                        self.rect.bottom = bottom

            else:
                self.currentJumpFrame = 0
                if now - self.lastUpdate > 200:
                    self.lastUpdate = now
                    bottom = self.rect.bottom
                    if self.facing == 'Left':
                        self.playCrouchSound = True
                        self.image = self.standingFrame[1]
                    elif self.facing == 'Right':
                        self.playCrouchSound = True
                        self.image = self.standingFrame[0]

                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom

        self.mask = pg.mask.from_surface(self.image)


class Mario(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.health = 3
        self.deadTimer = 0
        self.dead = False
        self.walking = False
        self.jumping = False
        self.playIceSound = True
        self.playCrouchSound = True
        self.crouching = False
        self.currentFrame = 0
        self.lastUpdate = 0
        self.crouchTimer = 0
        self.loadImages()
        self.facing = 'Right'
        self.hit = False
        self.image = self.standingFrame[0]
        self.currentJumpFrame = 0
        self.currentFrame = 0
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        self.pos = vec(width / 2 + 50, height / 2 )
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.mask = pg.mask.from_surface(self.image)

    def loadImages(self):
        sheet = spritesheet("sprites/loogi.png", "sprites/loogi.xml")

        self.standingFrame = [sheet.getImageName("mario_standing.png"),
                              pg.transform.flip(sheet.getImageName("mario_standing.png"), True, False)]

        self.walkingFramesRight = [sheet.getImageName("mario_walking_1.png"),
                                   sheet.getImageName("mario_walking_2.png"),
                                   sheet.getImageName("mario_walking_3.png"),
                                   sheet.getImageName("mario_walking_4.png"),
                                   sheet.getImageName("mario_walking_5.png"),
                                   sheet.getImageName("mario_walking_6.png"),
                                   sheet.getImageName("mario_walking_7.png"),
                                   sheet.getImageName("mario_walking_8.png"),
                                   sheet.getImageName("mario_walking_9.png"),
                                   sheet.getImageName("mario_walking_10.png"),
                                   sheet.getImageName("mario_walking_11.png"),
                                   sheet.getImageName("mario_walking_12.png")]
        self.walkingFramesLeft = []
        for frame in self.walkingFramesRight:
            self.walkingFramesLeft.append(pg.transform.flip(frame, True, False))

        self.jumpingFramesRight = [sheet.getImageName("mario_jumping.png")]

        self.jumpingFramesLeft = []
        for frame in self.jumpingFramesRight:
            self.jumpingFramesLeft.append(pg.transform.flip(frame, True, False))

        self.iceFramesRight = [sheet.getImageName("mario_scared_1.png"),
                               sheet.getImageName("mario_scared_2.png"),
                               sheet.getImageName("mario_scared_3.png"),
                               sheet.getImageName("mario_scared_4.png"),
                               sheet.getImageName("mario_scared_5.png"),
                               sheet.getImageName("mario_scared_6.png")]

        self.iceFramesLeft = []
        for frame in self.iceFramesRight:
            self.iceFramesLeft.append(pg.transform.flip(frame, True, False))

        self.deadFrames = sheet.getImageName("mario_dead.png")

    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
            if not self.jumping and not self.crouching:
                self.vel.y -= jumpPower

                self.game.jumpSound.play()
                self.jumping = True
            if not self.jumping and self.crouching:
                self.vel.y -= jumpPower / 2

                self.game.hopSound.play()

        if self.game.jumpOffEnemy < 10:
            if not self.jumping and not self.crouching:
                self.vel.y -= (jumpPower / 2)

                self.game.jumpSound.play()
                self.jumping = True
                self.game.jumpOffEnemy = 100

    def update(self):
        self.animate()
        self.acc = vec(0, playerGrav)
        keys = pg.key.get_pressed()
        if not self.hit:

            if keys[pg.K_LEFT] and not self.crouching:
                if not self.crouching:
                    self.acc.x = -playerAcc
                    self.facing = "Left"
                    if keys[pg.K_RCTRL]:
                        self.acc.x = playerAcc * -2
            if keys[pg.K_RIGHT] and not self.crouching:
                if not self.crouching:
                    self.acc.x = playerAcc
                    self.facing = "Right"
                    if keys[pg.K_RCTRL]:
                        self.acc.x = playerAcc * 2

        self.acc.x += self.vel.x * self.game.playerFriction
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if self.pos.x > width + 15:
            self.pos.x = -15
        if self.pos.x < -15:
            self.pos.x = width + 15
        self.rect.midbottom = self.pos
        if self.game.going:
            self.rect.y += self.game.platformSpeed

        self.crouchTimer += 1

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0 and not self.crouching:
            self.walking = True
        else:
            self.walking = False

        if self.hit and self.deadTimer < fps:
            self.image = self.deadFrames
            self.deadTimer += 1
            self.rect = self.image.get_rect()
        elif self.hit and self.deadTimer == fps and self.health > 0:
            self.jumping = True
            pg.mixer.Sound.play(self.game.hopSound)
            self.vel.y -= jumpPower / 3
            self.game.dieSound = False
            self.hit = False
            self.deadTimer = 0

        if not self.hit:
            if self.jumping or self.game.jumpOffEnemy < 10:
                self.playCrouchSound = True
                if now - self.lastUpdate > 100:
                    self.lastUpdate = now
                    if self.currentJumpFrame < len(self.jumpingFramesRight) - 1:
                        self.currentJumpFrame = (self.currentJumpFrame + 1)
                    bottom = self.rect.bottom
                    if self.facing == "Right":
                        self.image = self.jumpingFramesRight[self.currentJumpFrame]
                    elif self.facing == 'Left':
                        self.image = self.jumpingFramesLeft[self.currentJumpFrame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom

            elif self.walking:
                self.currentJumpFrame = 0
                self.playCrouchSound = True
                if self.game.playerFriction == -0.07:
                    if now - self.lastUpdate > 50:
                        self.lastUpdate = now
                        self.currentFrame = (self.currentFrame + 1) % len(self.walkingFramesRight)
                        bottom = self.rect.bottom
                        if self.vel.x > 0:
                            self.image = self.walkingFramesRight[self.currentFrame]
                            self.playIceSound = True
                        else:
                            self.image = self.walkingFramesLeft[self.currentFrame]
                            self.playIceSound = True
                        self.rect = self.image.get_rect()
                        self.rect.bottom = bottom
                    if abs(self.vel.x) < 0.7:
                        self.vel.x = 0

                else:
                    if now - self.lastUpdate > 40:
                        self.lastUpdate = now
                        self.currentFrame = (self.currentFrame + 1) % len(self.iceFramesRight)
                        bottom = self.rect.bottom
                        if self.vel.x > 0:
                            self.image = self.iceFramesRight[self.currentFrame]
                            if self.playIceSound:
                                self.game.iceSound.play()
                                self.playIceSound = False
                        else:
                            self.image = self.iceFramesLeft[self.currentFrame]
                            if self.playIceSound:
                                self.game.iceSound.play()
                                self.playIceSound = False
                        self.rect = self.image.get_rect()
                        self.rect.bottom = bottom

            else:
                self.currentJumpFrame = 0
                if now - self.lastUpdate > 200:
                    self.lastUpdate = now
                    bottom = self.rect.bottom
                    if self.facing == 'Left':
                        self.playCrouchSound = True
                        self.image = self.standingFrame[1]
                    elif self.facing == 'Right':
                        self.playCrouchSound = True
                        self.image = self.standingFrame[0]

                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom

        self.mask = pg.mask.from_surface(self.image)


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, color, width):
        pg.sprite.Sprite.__init__(self)
        self.color = color
        self.image = pg.Surface((0, 0))
        self.rect = self.image.get_rect()

        sheet = spritesheet("sprites/loogi.png", "sprites/loogi.xml")

        self.ice = sheet.getImageName("platform_ice.png")
        self.normal = sheet.getImageName("platform_no_ice.png")
        self.long = sheet.getImageName("platform_long_no_ice.png")
        self.longIce = sheet.getImageName("platform_long_ice.png")

        if color != 1:
            if width > 3:
                self.image = self.normal
            else:
                self.image = self.long
        elif color == 1:
            if width > 3:
                self.image = self.ice
            else:
                self.image = self.longIce

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y


class Fawfulcopter(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.sprites, game.fawfulcopters
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        sheet = spritesheet("sprites/loogi.png", "sprites/loogi.xml")

        self.sound = pg.mixer.Sound("sounds/fawfulcopter.ogg")
        self.soundPlaying = False

        self.idleFramesRight = [sheet.getImageName("fawfulcopter_idle_1.png"),
                                sheet.getImageName("fawfulcopter_idle_2.png"),
                                sheet.getImageName("fawfulcopter_idle_3.png"),
                                sheet.getImageName("fawfulcopter_idle_4.png"),
                                sheet.getImageName("fawfulcopter_idle_5.png"),
                                sheet.getImageName("fawfulcopter_idle_6.png"),
                                sheet.getImageName("fawfulcopter_idle_7.png"),
                                sheet.getImageName("fawfulcopter_idle_8.png"),
                                ]

        self.idleFramesLeft = []

        for frame in self.idleFramesRight:
            self.idleFramesLeft.append(pg.transform.flip(frame, True, False))

        self.deadFrames = [sheet.getImageName("fawfulcopter_dead.png"),
                           pg.transform.flip(sheet.getImageName("fawfulcopter_dead.png"), True, False)]

        self.image = self.idleFramesRight[0]
        self.currentFrame = 0
        self.lastUpdate = 0
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice([-100, width + 100])
        self.vx = random.randrange(3, 5)
        if self.rect.centerx > width:
            self.vx *= -1
        self.rect.y = random.randrange(-500, height / 8)
        self.vy = 0
        self.dy = 0.25
        self.hit = False
        self.mask = pg.mask.from_surface(self.image)
        self.alpha = 255
        self.playingSound = False

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        now = pg.time.get_ticks()
        if not self.hit:
            if now - self.lastUpdate > 20:
                if self.vx > 0:
                    self.lastUpdate = now
                    self.currentFrame = (self.currentFrame + 1) % len(self.idleFramesRight)
                    center = self.rect.center
                    self.image = self.idleFramesRight[self.currentFrame]
                    self.rect.center = center
                else:
                    self.lastUpdate = now
                    self.currentFrame = (self.currentFrame + 1) % len(self.idleFramesLeft)
                    center = self.rect.center
                    self.image = self.idleFramesLeft[self.currentFrame]
                    self.rect.center = center

            self.mask = pg.mask.from_surface(self.image)
        else:
            if now - self.lastUpdate > 20:
                if self.vx < 0:
                    center = self.rect.center
                    self.image = self.deadFrames[1]
                    self.vx = 0
                    self.vy = 0
                    self.rect.center = center
                elif self.vx > 0:
                    center = self.rect.center
                    self.image = self.deadFrames[0]
                    self.vx = 0
                    self.vy = 0
                    self.rect.center = center

                self.alpha -= 10

        if self.alpha <= 0:
            self.kill()

        if self.alpha == 255:
            if self.game.going:
                self.rect.y = self.rect.y + self.vy
            else:
                self.rect.y += self.vy

        if not self.game.pause:
            if not self.playingSound:
                self.sound.play(-1)
                self.playingSound = True

        if self.rect.left > width + 100 or self.rect.right < -100 or not self.game.playing:
            self.kill()
            self.sound.stop()


class Mushroom(pg.sprite.Sprite):
    def __init__(self, x, y, game):
        self.groups = game.sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = "Mushroom"
        sheet = spritesheet("sprites/loogi.png", "sprites/loogi.xml")
        self.image = sheet.getImageName("mushroom.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y


class oneUP(pg.sprite.Sprite):
    def __init__(self, x, y, game):
        self.groups = game.sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = "1UP"
        sheet = spritesheet("sprites/loogi.png", "sprites/loogi.xml")
        self.image = sheet.getImageName("1UP.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y


class enemyCoin(pg.sprite.Sprite):
    def __init__(self, x, y, game):
        self.starty = y
        self.groups = game.sprites, game.particles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.lastUpdate = 0
        self.currentFrame = 0
        sheet = spritesheet("sprites/loogi.png", "sprites/loogi.xml")
        self.image = sheet.getImageName("coin_1.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.frames = [sheet.getImageName("coin_1.png"),
                       sheet.getImageName("coin_2.png"),
                       sheet.getImageName("coin_3.png"),
                       sheet.getImageName("coin_4.png"),
                       sheet.getImageName("coin_5.png"),
                       sheet.getImageName("coin_6.png"),
                       sheet.getImageName("coin_7.png"),
                       sheet.getImageName("coin_8.png")
                       ]
        self.counter = 0

    def update(self):
        now = pg.time.get_ticks()
        if now - self.lastUpdate > 25:
            self.lastUpdate = now
            self.currentFrame = (self.currentFrame + 1) % len(self.frames)
            center = self.rect.center
            self.image = self.frames[self.currentFrame]
            self.rect = self.image.get_rect()
            self.rect.center = center

        if self.counter < fps * (1 / 3):
            self.counter += 1
        else:
            self.game.coinSound.play()
            self.kill()

        if self.counter < fps / 4:
            self.rect.y -= 10
