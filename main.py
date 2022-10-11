# from xml.dom.minidom import TypeInfo
import pygame
from sys import exit

# Import backend functions for components of the game.
import tile
import player

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Monopoly')
clock = pygame.time.Clock()

# Attempt to draw something on the pygame window.
#tileSurface = pygame.Surface((50, 50))
#tileSurface.fill('White')

gameRunning = True
jailIndex = 6

#bank instantiation


#put tiles in this array:
board = []
  
board.append(tile.Go(0))  # 0 is the tile index
board.append(tile.Property(1, 500, 25, 'b'))  # Syntax is: (tile index, buy price, rent price, space color)
board.append(tile.Property(2, 300, 40, 'b'))
board.append(tile.Property(3, 400, 50, 'b'))
board.append(tile.Property(4, 175, 15, 'g'))
board.append(tile.Property(5, 185, 20, 'g'))
board.append(tile.Jail(6))
board.append(tile.IncomeTax(7))
board.append(tile.LuxuryTax(8))
board.append(tile.Chance(9))
board.append(tile.CommunityChest(10))

#player array:
playerList = []

#get how many players
players = 4

#change when giving players piece selection if we do that
for i in range(players):
  playerList.append(player.Player(i)) # Create a player in the list, just incrementing the piece they are

#for i in range(len(board)):
#  screen.blit(tileSurface, (300, 100 * i))

# Main loop:
while gameRunning:
  #TESTING LOOP
  # Quits the game whenever the application window has been closed.

  for i in range(len(playerList)):
    turnFinished = False

    while not turnFinished:
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
          gameRunning = False
          pygame.quit()
          exit()

      playerList[i].move(board, playerList)
      
      cont = input("Enter 'go' to go to next player: ")
      if(cont == "go"):
        turnFinished = True

      pygame.display.update()
      clock.tick(60)
      
    print(f"Landed On Tile: {type(board[playerList[i].location])} at Location: {playerList[i].location}")
    print(f"Player {i} now has ${playerList[i].money}\n")