# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 00:51:53 2017
This manages the pygame logic that is decoupled from the game manager
@author: shashank
"""

import pygame, sys
import gamemanager

def main():
       pass
   

main()

 #Set up the game manager and screen for the game
win = ''
pygame.init()

size = width,height = 640,320 #Size of the world (in terms of pixels)


speed = [2,2] 
black = 0 , 0 , 0 
white = 255, 255 , 255

screen = pygame.display.set_mode(size) #Initialize the screen 
pygame.display.set_caption("A Fair World") #Define the caption for the window
clock = pygame.time.Clock() #Set the game clock

gm = gamemanager.gamemanager(screen,size[0],size[1],32)   

# Set up sprites for various objects
gamemanager.cell.setSprite(pygame.image.load("grass.png"))
gamemanager.food.setSprite(pygame.image.load("food.png"))

def playerRender(x,y): #Method to render the player at x , y
    screen.blit(playerImg, (x,y))

x = size[0]*0.5
y = size[1]*0.5
 
stop = False
print("Frame Rendered")
while not stop:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
    
    #screen.fill(white) #clear the screen (with white)
    screen.blit(gamemanager.food.sprite,(100,100))
    gm.display() #render the player
    
    pygame.display.update()
    clock.tick(60)
    print("Frame Rendered")

pygame.quit() #Quit pygame and python once out of the game loop
quit()