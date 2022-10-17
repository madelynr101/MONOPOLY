# from xml.dom.minidom import TypeInfo
from turtle import width
import pygame
from sys import exit

# Import backend functions for components of the game.
import tile
import player
import pygame_menu  

# setup main screen 
pygame.init()
screen = pygame.display.set_mode()
area = screen.get_rect()
pygame.display.set_caption('Monopoly')
clock = pygame.time.Clock()

# images and other references 
main_surface = pygame.image.load('Images/board3.png') # board image 

#image for character selection 
gauntlet = pygame.image.load('Images/gauntlet.png')
gauntlet = pygame.transform.scale(gauntlet,(35,35))
cape = pygame.image.load('Images/cape.png')
cape = pygame.transform.scale(cape,(35,35))
batcar = pygame.image.load('Images/batcar.png')
batcar = pygame.transform.scale(batcar,(35,35))
bat = pygame.image.load('Images/bat.png')
bat = pygame.transform.scale(bat,(35,35))

# size of main_surface 
width, height = main_surface.get_height(), main_surface.get_width()
print("area", area)
print("Height " +str(main_surface.get_height()))
print("Width " +str(main_surface.get_width()))

gameRunning = True
chosen = True

# player array:
playerList = []

#get how many players
players = 4
turnCount = 1

# player selection screen 
def player_screen():
  pass

# main game screen played 
def game():
  # change when giving players piece selection if we do that
  for i in range(players):
    playerList.append(player.Player(i)) # Create a player in the list, just incrementing the piece they are

  # Main loop:
  while gameRunning:
    # TESTING LOOP
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

    # output monopoly board 
    screen.blit(main_surface, (0,0)) 

    pygame.display.update()
    clock.tick(60)


def main():
  player_screen()
  game()
  pygame.quit()
  quit()


if __name__ == "__main__":
  main()