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
  
# Regular board is: Go, brown, community chest, brown, income tax, railroad, light blue, chance, light blue light blue, jail
# Purple, utilities, purple, purple, railroad, orange, community chest, orange, orange, free parking
# Red, chance, red, red, railroad, yellow, yellow, utilities, yellow, go to jail
# Green, green, community chest, green, railroad, chance, blue, luxary tax, blue, go

board.append(tile.Go(0))  # 0 is the tile index
board.append(tile.Property(1, 60, 2, 'Brown'))  # Syntax is: (tile index, buy price, rent price, space color)
board.append(tile.CommunityChest(2))
board.append(tile.Property(3, 60, 4, 'Brown'))
board.append(tile.IncomeTax(4))
board.append(tile.Property(5, 200, 25, 'Railroad'))
board.append(tile.Property(6, 100, 6, 'Cyan'))
board.append(tile.Chance(7))
board.append(tile.Property(8, 100, 6, 'Cyan'))
board.append(tile.Property(9, 120, 8, 'Cyan'))
board.append(tile.Jail(10))
board.append(tile.Property(11, 140, 10, 'Purple'))
board.append(tile.Property(12, 150, 4, 'Utility'))
board.append(tile.Property(13, 140, 10, 'Purple'))
board.append(tile.Property(14, 160, 12, 'Purple'))
board.append(tile.Property(15, 200, 25, 'Railroad'))
board.append(tile.Property(16, 180, 14, 'Orange'))
board.append(tile.CommunityChest(17))
board.append(tile.Property(18, 180, 14, 'Orange'))
board.append(tile.Property(19, 200, 16, 'Orange'))
board.append(tile.FreeParking(20))
board.append(tile.Property(21, 220, 18, 'Red'))
board.append(tile.Chance(22))
board.append(tile.Property(23, 220, 18, 'Red'))
board.append(tile.Property(24, 240, 20, 'Red'))
board.append(tile.Property(25, 200, 25, 'Railroad'))
board.append(tile.Property(26, 260, 22, 'Yellow'))
board.append(tile.Property(27, 260, 22, 'Yellow'))
board.append(tile.Property(28, 150, 4, 'Utility'))
board.append(tile.Property(29, 280, 24, 'Yellow'))
board.append(tile.GoToJail(30))
board.append(tile.Property(31, 300, 26, 'Green'))
board.append(tile.Property(32, 300, 26, 'Green'))
board.append(tile.CommunityChest(33))
board.append(tile.Property(34, 320, 28, 'Green'))
board.append(tile.Property(35, 200, 25, 'Railroad'))
board.append(tile.Chance(36))
board.append(tile.Property(37, 350, 35, 'Navy'))
board.append(tile.LuxuryTax(38))
board.append(tile.Property(39, 400, 50, 'Navy'))

#player array:
playerList = []

#get how many players
players = 4

turnCount = 1

#change when giving players piece selection if we do that
for i in range(players):
  playerList.append(player.Player(i)) # Create a player in the list, just incrementing the piece they are

#for i in range(len(board)):
#  screen.blit(tileSurface, (300, 100 * i))

# Main loop:
while gameRunning:
  #TESTING LOOP
  # Quits the game whenever the application window has been closed.

  print(f"Turn: {turnCount}")

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

    print(f"\nProperty List for Player {i}: {playerList[i].getProperties()}\n")

  turnCount += 1