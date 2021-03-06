# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 00:51:53 2017
This manages the pygame logic that is decoupled from the game manager
@author: shashank
"""

import pygame, sys
import gamemanager
import entity


def main():
    pass


main()

# Set up the game manager and screen for the game
win = ''
pygame.init()

size = width, height = 640, 320  # Size of the world (in terms of pixels)

speed = [2, 2]
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)  # Initialize the screen
pygame.display.set_caption("A Fair World")  # Define the caption for the window
clock = pygame.time.Clock()  # Set the game cock

gm = gamemanager.gamemanager(screen, size[0], size[1], 32)

# Set up sprites for various objects
entity.entity.setPPU(32)
gamemanager.cell.setSprite(pygame.image.load(r"Sprites/grass.png"))
gamemanager.food.setSprite(pygame.image.load(r"Sprites/food.png"))
gamemanager.player.setSprite(pygame.image.load(r"Sprites/player.png"))
gamemanager.scent.setSprite(pygame.image.load(r"Sprites/scent.png"))

# Game loop stop variable
stop = False

# Main game loop
while not stop:

    # Stop game when player closes the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True

    screen.fill(white)  # clear the screen (with white)

    gm.display()  # render the game using the game manager

    pygame.display.update()
    clock.tick(60)

pygame.quit()  # Quit pygame and python once out of the game loop
