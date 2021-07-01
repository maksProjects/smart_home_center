import pygame
import sys
from pygame.locals import *
import mainscreen
import intercomscreen
from deviceSetup import setupFile

pygame.init()
pygame.font.init()


screen_w = setupFile["main_settings"][0]["screen_w"]
screen_h = setupFile["main_settings"][0]["screen_h"]
fullscreen = setupFile["main_settings"][0]["fullscreen"]
fontcolor = setupFile["main_settings"][0]["fontcolor"]
font = "./assets/fonts/roboto/Roboto-Regular.ttf"

# BACKGROUND
background = pygame.image.load("assets/backgrounds/b4.jpg")
background = pygame.transform.scale(background, (screen_w, screen_w))

# SCREENS
screen = pygame.display.set_mode((screen_w, screen_h), 0, 32)
pygame.display.set_caption('smart home center')
firstscreen = mainscreen.Screen(screen_w, screen_h, font, fontcolor)
firstscreen.set_colorkey((0, 0, 0))
rightscreen = intercomscreen.Screen(screen_w, screen_h, font, fontcolor)
rightscreen.set_colorkey((0, 0, 0))

# which screen
animation = False
numberOfScreens = 1   # counts from 0, so numberOfScreens = 1 means there are 2 screens
whichScreen = 0

while True:
    # Events
    for event in pygame.event.get():
        # APP QUIT
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit(0)

        # INTERCOM CHECK
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            whichScreen = 1

        # FULLSCREEN TOGGLE
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            if fullscreen == 0:
                screen = pygame.display.set_mode((screen_w, screen_h), FULLSCREEN, 32)
                fullscreen = 1
            else:
                screen = pygame.display.set_mode((screen_w, screen_h), 0, 32)
                fullscreen = 0

        # SWITCHING BETWEEN SCREENS
        elif not animation:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if whichScreen == numberOfScreens:
                    whichScreen = 0
                else:
                    whichScreen += 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if whichScreen == 0:
                    whichScreen = 1
                else:
                    whichScreen -= 1

    # DRAW
    # reset the screen
    screen.blit(background, (0, 0))
    if whichScreen == 0:
        firstscreen.draw()
        screen.blit(firstscreen, (0, 0))
    elif whichScreen == 1:
        rightscreen.draw()
        screen.blit(rightscreen, (0, 0))

    # flip the display
    pygame.display.flip()
