# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 00:51:53 2017
This manages the pygame logic that is decoupled from the game manager
@author: shashank
"""

import pygame, sys
import gamemanager

def main():
    
    #Set up the game manager and screen for the game
    win = ''
    pygame.init()
    
    size = width,height = 320,240 #Size of the world (in terms of pixels)

    gm = gamemanager.gamemanager(win,size[0],size[1],10)   

    speed = [2,2] 
    black = 0 , 0 , 0 

    screen = pygame.display.set_mode(size) #Initialize the screen 
    pygame.display.set_caption("A Fair World")    
    
   
     

main()