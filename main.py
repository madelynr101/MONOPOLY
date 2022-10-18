# from xml.dom.minidom import TypeInfo
from turtle import width
import pygame
from sys import exit

# Import backend functions for components of the game.
import tile
import player 


# Purpose: To pick how many players and / or AI's there are within the game
def choose_people():
  pass 

# Purpose: To display player name, properties, money, etc. 
def display_amounts():
  pass 

# Purpose: To display dice roll screen and the dice after the roll 
def roll():
  pass

# Purpose: To display buy property 
def property_buy():
  pass

# Purpose: To diplay game over button 
def game_over():
  pass 

# Purpose: To show how much money someone gets paid after they land on their property 
def get_paid():
  pass 

# Purpose: Show when someone gets sent to jail 
def jail():
  pass 

# HENRY'S PART 
# Purpose: To choose the character for each person, either human or AI. 
def player_loop():
  #image for character selection 
  gauntlet = pygame.image.load('Images/gauntlet.png')
  gauntlet = pygame.transform.scale(gauntlet,(35,35))
  cape = pygame.image.load('Images/cape.png')
  cape = pygame.transform.scale(cape,(35,35))
  batcar = pygame.image.load('Images/batcar.png')
  batcar = pygame.transform.scale(batcar,(35,35))
  bat = pygame.image.load('Images/bat.png')
  bat = pygame.transform.scale(bat,(35,35))
  pass 

  
def main():
  # setup main screen 
  pygame.init()
  screen = pygame.display.set_mode((1000, 1000), pygame.RESIZABLE)
  area = screen.get_rect()
  pygame.display.set_caption('Monopoly')
  clock = pygame.time.Clock()


  # images and other references 
  main_surface = pygame.image.load('Images/board.png') # board image 


  # size of main_surface 
  width, height = main_surface.get_height(), main_surface.get_width()
  print("area", area)
  print("Height " + str(height))
  print("Width " + str(width))


  gameRunning = True
  chosen = True
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
    playerList.append(player.Player(i, True)) # Create a player in the list, just incrementing the piece they are

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

        screen.blit(main_surface, (0,0))
        

        pygame.display.update()
        clock.tick(60)

        """
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
    """
if __name__ == "__main__":
  main()