import random

random.seed()

width = 1080
height = 720
fps = 60
title = "Luigi's Adventure"
font = 'Main.otf'
saveFile = "Save/" + str(title) + ".ini"
spriteSheet = "loogi.png"

playerAcc = 0.7
minFriction = -0.00001
maxFriction = -0.07
playerGrav = 1.5
jumpPower = 33

mobSpawnRate = 10000

platformList = [(random.randrange(0, width - 300), 100, random.randrange(5, 10), 1),
                (width / 2 - 150, height / 2, random.randrange(5, 10), 1),
                (random.randrange(0, width - 300), -150, random.randrange(5, 10), 1),
                ]

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
lightBlue = (0, 153, 153)
sansEye = (132, 255, 242)
bgColor = list(lightBlue)
