import pygame
import random
#from datetime import datetime

# Import backend functions for components of the game.
import tile
import player
import card

# Seeds RNG based off of the computer's internal clock.
#random.seed(datetime.now())

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Monopoly')
clock = pygame.time.Clock()

gameRunning = True

#put tiles in this array:
board = []

#player array:
playerList = []

#get how many players
players = 4

#change when giving players piece selection if we do that
for i in range(players-1):
  playerList.append(player(i))#create a player in the list, just incrementing the piece they are



# Main loop:
while gameRunning:
  # Quits the game whenever the application window has been closed.
  for e in pygame.event.get():
    if e.type == pygame.QUIT:
      pygame.quit()
      exit()

  pygame.display.update()
  clock.tick(60)