import pygame
#from datetime import datetime

# Import backend functions for components of the game.
import tile
import player

# Seeds RNG based off of the computer's internal clock.
#random.seed(datetime.now())

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Monopoly')
clock = pygame.time.Clock()

gameRunning = True
jailIndex = 6

#bank instantiation


#put tiles in this array:
board = []
  
board.append(tile.GO(0))  # 0 is the tile index
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
for i in range(players-1):
  playerList.append(player(i))#create a player in the list, just incrementing the piece they are



# Main loop:
while gameRunning:
  # Quits the game whenever the application window has been closed.
  #TESTING LOOP
  
  for i in range(len(playerList)):
    turnFinished = False
    while not turnFinished:
      playerList[i].move(board)
      
      cont = input("Enter 'go' to go to next player: ")
      if(cont == "go"):
        turnFinished = True
      
    print("Player " + i + ": now has $" + playerList[i].money + "\n")

  continue
  
  # for e in pygame.event.get():
  #   if e.type == pygame.QUIT:
  #     pygame.quit()
  #     exit()

  # pygame.display.update()
  # clock.tick(60)