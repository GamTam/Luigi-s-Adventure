import math
import os
import sys
import pygame

sansEye = pygame.image.load("sprites/sans_eye.png")
pygame.display.set_icon(sansEye)

pygame.mixer.init(48000, -16, 2, 1024)
pygame.init()
pygame.display.set_caption("SAAAAAAAAAAAAAAAAAAAANS")

screen = pygame.display.set_mode((640, 480))
screen.fill((0, 0, 0))
clock = pygame.time.Clock()
j = 1
head = 0
song_playing = ""
pause = False
pauseSound = False
pauseDown = False
click = pygame.mixer.Sound("sounds/click.ogg")
progress = 0

x = 0
y = 0
vel = 5

# load sprites
bg = pygame.image.load("sprites/bg.png")
pauseImage = pygame.image.load("sprites/pause.png")
sansHead = pygame.image.load("sprites/sans_head.png").convert_alpha()
sansTorso = pygame.image.load("sprites/sans_torso.png").convert_alpha()
sansLegs = pygame.image.load("sprites/sans_legs.png").convert_alpha()


def sans(x, y):
    headMovementX = [x, x, x - 1, x - 1, x - 1, x - 1, x, x, x, x + 1, x + 1, x + 1, x + 1, x + 1]
    headMovementY = [y, y - 1, y - 1, y - 1, y, y + 1, y + 1, y, y - 1, y - 1, y - 1, y, y + 1, y + 1]
    bodyMovementX = [x - 11, x - 11, x - 12, x - 12, x - 12, x - 12, x - 11, x - 11, x - 11, x - 10, x - 10, x - 10,
                     x - 10, x - 10]
    bodyMovementY = [y, y, y - 1, y, y, y + 1, y, y, y, y - 1, y, y, y + 1, y + 1]
    global head
    global j
    global sansHead
    global sansTorso
    global sansLegs

    if not pause:
        if math.floor(j) == len(headMovementX) - 1 or j == 0:
            head += 1

        if math.floor(j) <= len(headMovementX) - 1 and (head % 2) == 0:
            j += 0.25
        elif math.floor(j) >= 0 and (head % 2) == 1:
            j -= 0.25

    screen.blit(sansLegs, (x - 4, y + 49))
    screen.blit(sansTorso, (bodyMovementX[math.floor(j)], bodyMovementY[math.floor(j)] + 25))
    screen.blit(sansHead, (headMovementX[math.floor(j)], headMovementY[math.floor(j)]))


def image():
    bar = Bar()
    screen.blit(bg, (0, 0))
    sans(x, y)
    bar.draw()
    if pause:
        screen.blit(pauseImage, (0, 0))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(15, 400, 600, 20), 2)
    pygame.display.update()


def play_music(name, intro):
    pygame.mixer.pre_init(48000, -16, 2, 4096)
    global song_playing
    global pauseSound

    if pause:
        if pauseSound:
            click.play(0)
            pauseSound = False
        pygame.mixer.music.pause()
    else:
        if pauseSound:
            click.play(0)
            pauseSound = False
        pygame.mixer.music.unpause()

    if intro:
        if song_playing != "loop":
            if not pygame.mixer.music.get_busy() and song_playing == "":
                if song_playing == "":
                    pygame.mixer.music.load("music/" + str(name) + "_intro.ogg")
                    song_playing = "intro"
                    pygame.mixer.music.play()
            elif pygame.mixer.music.get_pos() == -1:
                pygame.mixer.music.load("music/" + str(name) + "_main.ogg")
                pygame.mixer.music.play(-1)
                song_playing = "loop"
    else:
        if song_playing != "loop":
            if pygame.mixer.music.get_pos() == -1:
                pygame.mixer.music.load("music/" + str(name) + ".ogg")
                pygame.mixer.music.play(-1)
                song_playing = "loop"


def player_movement(direction):
    global x
    global y

    if direction == "Up":
        y -= vel
    elif direction == "Down":
        y += vel
    elif direction == "Left":
        x -= vel
    elif direction == "Right":
        x += vel



class Bar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = pygame.sprite.Group()
        self.image = pygame.Surface((0 + progress, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 15
        self.rect.y = 400
        self.sprites.add(self)

    def draw(self):
        self.sprites.draw(screen)

downing = False

while True:
    image()
    clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            print(head)
            pygame.quit()
            sys.exit()

    pygame.display.flip()

    if not pause:
        if keys[pygame.K_w]:
            player_movement("Up")
        if keys[pygame.K_s]:
            player_movement("Down")
        if keys[pygame.K_a]:
            player_movement("Left")
        if keys[pygame.K_d]:
            player_movement("Right")

        if keys[pygame.K_SPACE]:
            break

    if keys[pygame.K_LSHIFT] and not pause and not pauseDown:
        pause = True
        pauseDown = True
        pauseSound = True
    elif keys[pygame.K_LSHIFT] and pause and not pauseDown:
        pause = False
        pauseDown = True
        pauseSound = True
    elif not keys[pygame.K_LSHIFT] and pauseDown:
        pauseDown = False

    play_music("galeem", True)

    if progress < 600 and downing == False:
        progress += 5
    elif progress != 0 and downing == True:
        progress -= 5

    if progress == 600:
        downing = True
    if progress == 0:
        downing = False
