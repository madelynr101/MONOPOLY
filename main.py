import pygame
import random
from datetime import datetime

# Import backend functions for components of the game.
import tile
import player
import card

# Seeds RNG based off of the computer's internal clock.
random.seed(datetime.now())

pygame.init()

gameRunning = True

# Main loop:
while gameRunning:

  # Quits the game whenever the application window has been closed.
  for e in pygame.event.get():
    if e.type == pygame.QUIT:
      gameRunning = False

pygame.quit()