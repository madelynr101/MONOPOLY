# from xml.dom.minidom import TypeInfo
from turtle import width
import pygame
from sys import exit

# Import backend functions for components of the game.
import tile
import player


# Initialize pygame so we can initialize font
pygame.init()

# Default font
font: pygame.font = pygame.font.SysFont("arialblack", 40)

# Default text color
TEXT_COL = (0, 0, 0)
PLAYER_COLS: list[tuple[int]] = [
    (224, 49, 22),
    (42, 176, 12),
    (40, 48, 209),
    (209, 155, 46),
]

# Text draw function
def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Use to create and draw buttons using images
class Button:
    def __init__(self, x, y, image, scale):
        self.image = pygame.transform.scale(image, scale)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, screen):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


# Purpose: To pick how many players and / or AI's there are within the game
def choose_people():
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
def player_loop(screen, playerList, playersChosen):
    availablePieces = [True] * 4
    while playersChosen < len(playerList):
        print(playersChosen)
        screen.fill((255, 255, 255))
        # image for character selection
        gauntlet = pygame.image.load("Images/gauntlet.png")
        cape = pygame.image.load("Images/cape.png")
        batcar = pygame.image.load("Images/batcar.png")
        bat = pygame.image.load("Images/bat.png")

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                gameRunning = False
                pygame.quit()
                exit()

        draw_text(
            screen,
            f"Please select the piece for player {playersChosen + 1}",
            font,
            TEXT_COL,
            150,
            100,
        )
        gauntletButton = Button(150, 500, gauntlet, (100, 100))
        capeButton = Button(350, 500, cape, (100, 100))
        batcarButton = Button(550, 500, batcar, (100, 100))
        batButton = Button(750, 500, bat, (100, 100))
        buttons = [gauntletButton, capeButton, batcarButton, batButton]

        for i in range(4):
            if availablePieces[i]:
                if buttons[i].draw(screen):
                    availablePieces[i] = False
                    playerList[playersChosen].piece = i
                    playersChosen += 1

        pygame.display.update()


def pick_piece(playerIndex, pieceIndex):
    pass


def load_tiles(board):
    # Regular board is: Go, brown, community chest, brown, income tax, railroad, light blue, chance, light blue light blue, jail
    # Purple, utilities, purple, purple, railroad, orange, community chest, orange, orange, free parking
    # Red, chance, red, red, railroad, yellow, yellow, utilities, yellow, go to jail
    # Green, green, community chest, green, railroad, chance, blue, luxary tax, blue, go

    board.append(tile.Go(0))  # 0 is the tile index
    board.append(
        tile.Property(1, 60, 2, "Brown")
    )  # Syntax is: (tile index, buy price, rent price, space color)
    board.append(tile.CommunityChest(2))
    board.append(tile.Property(3, 60, 4, "Brown"))
    board.append(tile.IncomeTax(4))
    board.append(tile.Property(5, 200, 25, "Railroad"))
    board.append(tile.Property(6, 100, 6, "Cyan"))
    board.append(tile.Chance(7))
    board.append(tile.Property(8, 100, 6, "Cyan"))
    board.append(tile.Property(9, 120, 8, "Cyan"))
    board.append(tile.Jail(10))
    board.append(tile.Property(11, 140, 10, "Purple"))
    board.append(tile.Property(12, 150, 4, "Utility"))
    board.append(tile.Property(13, 140, 10, "Purple"))
    board.append(tile.Property(14, 160, 12, "Purple"))
    board.append(tile.Property(15, 200, 25, "Railroad"))
    board.append(tile.Property(16, 180, 14, "Orange"))
    board.append(tile.CommunityChest(17))
    board.append(tile.Property(18, 180, 14, "Orange"))
    board.append(tile.Property(19, 200, 16, "Orange"))
    board.append(tile.FreeParking(20))
    board.append(tile.Property(21, 220, 18, "Red"))
    board.append(tile.Chance(22))
    board.append(tile.Property(23, 220, 18, "Red"))
    board.append(tile.Property(24, 240, 20, "Red"))
    board.append(tile.Property(25, 200, 25, "Railroad"))
    board.append(tile.Property(26, 260, 22, "Yellow"))
    board.append(tile.Property(27, 260, 22, "Yellow"))
    board.append(tile.Property(28, 150, 4, "Utility"))
    board.append(tile.Property(29, 280, 24, "Yellow"))
    board.append(tile.GoToJail(30))
    board.append(tile.Property(31, 300, 26, "Green"))
    board.append(tile.Property(32, 300, 26, "Green"))
    board.append(tile.CommunityChest(33))
    board.append(tile.Property(34, 320, 28, "Green"))
    board.append(tile.Property(35, 200, 25, "Railroad"))
    board.append(tile.Chance(36))
    board.append(tile.Property(37, 350, 35, "Navy"))
    board.append(tile.LuxuryTax(38))
    board.append(tile.Property(39, 400, 50, "Navy"))


def main():
    # setup main screen

    screen: pygame.display = pygame.display.set_mode((1000, 1000), pygame.RESIZABLE)
    area = screen.get_rect()
    pygame.display.set_caption("Monopoly")
    clock = pygame.time.Clock()

    # images and other references
    main_surface = pygame.image.load("Images/board.png")  # board image

    # size of main_surface
    width, height = main_surface.get_height(), main_surface.get_width()
    print("area", area)
    print("Height " + str(height))
    print("Width " + str(width))

    gameRunning = True
    chosen = True
    jailIndex = 6

    # bank instantiation

    # put tiles in this array:
    board = []

    load_tiles(board)

    # player array:
    playerList = []

    # get how many players
    players = 4

    turnCount = 1
    # change when giving players piece selection if we do that
    for i in range(players):
        playerList.append(
            player.Player(i, True)
        )  # Create a player in the list, just incrementing the piece they are

    # for i in range(len(board)):
    #  screen.blit(tileSurface, (00, 100 * i))

    # playersChosen = 0
    # if playersChosen < players:
    #     player_loop(screen, playerList, playersChosen)

    endTurnImage = pygame.image.load("Images/endTurn.png")
    endTurnButton = Button(width / 7, height / 1.26, endTurnImage, (200, 50))

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

                screen.blit(main_surface, (0, 0))
                playerList[i].displayAmounts(
                    screen, font, PLAYER_COLS[i], (width, height), i
                )

                if endTurnButton.draw(screen):
                    turnFinished = True

                pygame.display.update()
                clock.tick(60)
        turnCount += 1


if __name__ == "__main__":
    main()
