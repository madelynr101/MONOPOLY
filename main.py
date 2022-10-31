# from xml.dom.minidom import TypeInfo
from turtle import width
import pygame
from sys import exit
from draw import Button, draw_text
import time

# Import backend functions for components of the game.
import tile
import player


# Initialize pygame so we can initialize font
pygame.init()

# Default font
font: pygame.font.Font = pygame.font.SysFont("arialblack", 40)

# Default text color
TEXT_COL: tuple[int, int, int] = (0, 0, 0)

# Each player has a unique text color
PLAYER_COLS: list[tuple[int, int, int]] = [
    (224, 49, 22),
    (42, 176, 12),
    (40, 48, 209),
    (209, 155, 46),
]

# The locations to draw the bought property markers
PROPERTY_LOCATIONS: list[tuple[int, int]] = [
    (0, 0),
    (827, 940),
    (0, 0),
    (663, 940),
    (0, 0),
    (500, 940),
    (417, 940),
    (0, 0),
    (254, 940),
    (172, 940),
    (0, 0),
    (60, 828),
    (60, 745),
    (60, 664),
    (60, 582),
    (60, 500),
    (60, 417),
    (0, 0),
    (60, 252),
    (60, 172),
    (0, 0),
    (172, 60),
    (0, 0),
    (336, 60),
    (417, 60),
    (500, 60),
    (582, 60),
    (663, 60),
    (746, 60),
    (827, 60),
    (0, 0),
    (940, 172),
    (940, 254),
    (0, 0),
    (940, 417),
    (940, 500),
    (0, 0),
    (940, 664),
    (0, 0),
    (940, 828),
]

# The locations to draw the player icons on each space
PLAYER_LOCATIONS: list[list[tuple[int, int]]] = [
    [(870, 880), (940, 880), (870, 945), (940, 945)],
    [(785, 880), (825, 880), (785, 945), (825, 945)],
    [(705, 880), (745, 880), (705, 945), (745, 945)],
    [(622, 880), (663, 880), (622, 945), (663, 945)],
    [(540, 880), (581, 880), (540, 945), (581, 945)],
    [(458, 880), (499, 880), (458, 945), (499, 945)],
    [(376, 880), (417, 880), (376, 945), (417, 945)],
    [(294, 880), (335, 880), (294, 945), (335, 945)],
    [(212, 880), (253, 880), (212, 945), (253, 945)],
    [(130, 880), (171, 880), (130, 945), (171, 945)],
    [(0, 870), (0, 930), (40, 960), (90, 960)],
    [(90, 787), (90, 827), (0, 787), (0, 827)],
    [(90, 705), (90, 745), (0, 705), (0, 745)],
    [(90, 623), (90, 663), (0, 623), (0, 663)],
    [(90, 541), (90, 581), (0, 541), (0, 581)],
    [(90, 459), (90, 499), (0, 459), (0, 499)],
    [(90, 377), (90, 417), (0, 377), (0, 417)],
    [(90, 295), (90, 335), (0, 295), (0, 335)],
    [(90, 213), (90, 253), (0, 213), (0, 253)],
    [(90, 131), (90, 171), (0, 131), (0, 171)],
    [(90, 80), (0, 80), (90, 10), (0, 10)],
    [(175, 80), (134, 80), (175, 10), (134, 10)],
    [(257, 80), (216, 80), (257, 10), (216, 10)],
    [(339, 80), (298, 80), (339, 10), (298, 10)],
    [(421, 80), (380, 80), (421, 10), (380, 10)],
    [(503, 80), (462, 80), (503, 10), (462, 10)],
    [(585, 80), (544, 80), (585, 10), (544, 10)],
    [(667, 80), (626, 80), (667, 10), (626, 10)],
    [(749, 80), (708, 80), (749, 10), (708, 10)],
    [(831, 80), (790, 80), (831, 10), (790, 10)],
    [(870, 80), (870, 10), (950, 80), (950, 10)],
    [(870, 175), (870, 134), (950, 175), (950, 134)],
    [(870, 257), (870, 216), (950, 257), (950, 216)],
    [(870, 339), (870, 298), (950, 339), (950, 298)],
    [(870, 421), (870, 380), (950, 421), (950, 380)],
    [(870, 503), (870, 462), (950, 503), (950, 462)],
    [(870, 585), (870, 544), (950, 585), (950, 544)],
    [(870, 667), (870, 626), (950, 667), (950, 626)],
    [(870, 749), (870, 708), (950, 749), (950, 708)],
    [(870, 831), (870, 790), (950, 831), (950, 790)],
]

PIECE_IMAGES: list[pygame.surface.Surface] = [
    pygame.image.load("Images/gauntlet.png"),
    pygame.image.load("Images/cape.png"),
    pygame.image.load("Images/batmobile.png"),
    pygame.image.load("Images/bat.png"),
]


# Purpose: To pick how many players and / or AI's there are within the game
def chooseAIPlayers(screen):
    # whether a person has picked how many players they want, AI or human 
    chosen = False 

    # images for player selection:
    zero = pygame.image.load("Images/0.png")
    one = pygame.image.load("Images/1.png")
    two = pygame.image.load("Images/2.png")
    three = pygame.image.load("Images/3.png")
    four = pygame.image.load("Images/4.png")

    zeroButton = Button(50, 500, zero, (80, 80))
    oneButton = Button(250, 500, one, (80, 80))
    twoButton = Button(450, 500, two, (80, 80))
    threeButton = Button(650, 500, three, (80, 80))
    fourButton = Button(850, 500, four, (80, 80))
    buttons = [zeroButton, oneButton, twoButton, threeButton, fourButton]

    # Choose amount of AI players:
    while chosen != True:
        screen.fill((255, 255, 255))

        # Quit if the X button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
                pygame.quit()
                quit()

        draw_text(
            screen,
            f"How many AI players do you want 0-4?",
            font,
            TEXT_COL,
            20,
            20,
        )

        # player buttons output to screen and data collected
        for i in range(len(buttons)):
            buttons[i].draw(screen)
            if buttons[i].clicked:
                return i  # Returns the button pressed, the number of AI player we want 

        pygame.display.update()


# Matt Chenot
# Purpose: To display dice roll screen and the dice after the roll
def rollDisplay(screen: pygame.surface.Surface, text_color: tuple[int, int, int], screen_size: tuple[int, int], currentPlayer: player):
    # NOTE: think on moving this to the roll function, that way the popup can show up for the jail stuff to
    # NOTE: I have yet to figure out the more complicated version of this, so here is a simple one for now

    diceImageList = []
    scaledDiceImageList = []
    diceImageList.append(pygame.image.load("Images/dice1.png"))
    diceImageList.append(pygame.image.load("Images/dice2.png"))
    diceImageList.append(pygame.image.load("Images/dice3.png"))
    diceImageList.append(pygame.image.load("Images/dice4.png"))
    diceImageList.append(pygame.image.load("Images/dice5.png"))
    diceImageList.append(pygame.image.load("Images/dice6.png"))

    for image in diceImageList:  # Scale the images to be smaller
        scaledDiceImageList.append(pygame.transform.scale(image, (80, 80)))

    smallerFont: pygame.font.Font = pygame.font.SysFont("arialblack", 25)
    
    # Does the actual display
    draw_text(screen, f"Roll:", smallerFont, text_color, screen_size[0] / 1.73, screen_size[1] / 2)
    screen.blit(scaledDiceImageList[currentPlayer.getLastRoll()[0]-1], (screen_size[0] / 1.55, screen_size[1] / 2))
    screen.blit(scaledDiceImageList[currentPlayer.getLastRoll()[1]-1], (screen_size[0] / 1.35, screen_size[1] / 2))


# Henry
# Purpose: To diplay game over button
def game_over():
    pass


# Madelyn Weathers
# Purpose: To show how much money someone gets paid after they land on their property
def get_paid():
    pass


# Ethan Moore
# Purpose: Show when someone gets sent to jail, chose to attempt a roll or pay $50 to get out
def jail(prisoner: int):  # NOTE: This is currently never called
    choiceMade = False
    escapeImage = pygame.image.load("Images/escapeButton.png")
    payImage = pygame.image.load("Images/payButton.png")
    useCardImage = pygame.image.load("Images/cardButton.png")
    # TODO: ensure buttons properly display
    while not choiceMade:
        draw_text(screen, f"How do you want to leave jail?", font, TEXT_COL, 20, 20)
        escapeButton = Button(50, 100, escapeImage, (50, 100))
        payButton = Button(150, 100, payImage, (50,100))
        cardButton = Button(250, 100, useCardImage, (50,100))

        if escapeButton.draw():
            playerList[prisioner].move()
            choiceMade = True
        if prisoner.money > 50:
            if payButton.draw():
                playerList[prisoner].bankTransaction(-50)
                playerList[prisoner].isInJail = False
                choiceMade = True
                playerList[prisoner].move()
        if prisoner.getOutOfJailCards > 0:
            if cardButton.draw():
                playerList[prisoner].isInJail = False
                playerList[prisoner].getOutOfJailCards -= 1
                choiceMade = True
                playerList[prisoner].move()


# HENRY'S PART
# Purpose: To choose the piece for each player
def choosePieces(screen: pygame.surface.Surface, playerList: list[player.Player]):
    playersChosen = 0
    
    availablePieces = [True] * 4
    while playersChosen < len(playerList):
        print(playersChosen)
        screen.fill((255, 255, 255))
        # image for character selection
        gauntlet = PIECE_IMAGES[0]
        cape = PIECE_IMAGES[1]
        batcar = PIECE_IMAGES[2]
        bat = PIECE_IMAGES[3]

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

        for i in range(len(PIECE_IMAGES)):
            if availablePieces[i]:
                if buttons[i].draw(screen):
                    availablePieces[i] = False
                    playerList[playersChosen].piece = i
                    playersChosen += 1

        pygame.display.update()


def pick_piece(playerIndex, pieceIndex):
    pass


# Tile types and locations are hardcoded, this puts them into the passed board
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
    screen: pygame.surface.Surface = pygame.display.set_mode(
        (1000, 1000), pygame.RESIZABLE
    )
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

    # put tiles in this array:
    board = []
    load_tiles(board)

    # player array:
    playerList: list[player.Player] = []

    # Always 4 players, always start on turn 1
    numPlayers = 4
    turnCount = 1

    # For testing purposes
    # playerProperties: list[list[tile.Property]] = [
    #     [board[1], board[5], board[13], board[23], board[34]],
    #     [board[3], board[15], board[21], board[32]],
    #     [board[6], board[11], board[24], board[31]],
    #     [board[8], board[18], board[26], board[37]],
    # ]

    # change when giving players piece selection if we do that
    for i in range(numPlayers):
        # For testing purposes
        # playerList.append(player.Player(i, True, playerProperties[i], 39))
        playerList.append(player.Player(i, False))  # Create a player in the list, just incrementing the piece they are

    # for i in range(len(board)):
    #  screen.blit(tileSurface, (00, 100 * i))

    # Figure out how many AI players there will be
    numAIPlayers = chooseAIPlayers(screen)

    # Mark the selected players as AI
    # This works from the end, so if you select 2 AI players, then players 3 and 4 will be AI
    for i in range(numAIPlayers):
        playerList[numPlayers - i - 1].setIsAI(True)  

    
    choosePieces(screen, playerList)  # Chose which player will be which piece

    # Button prep
    endTurnImage = pygame.image.load("Images/endTurn.png")
    endTurnButton = Button(width / 7, height / 1.26, endTurnImage, (200, 50))

    rollImage = pygame.image.load("Images/rollButton.png")
    rollButton = Button(width / 2.75, height / 1.26, rollImage, (200, 50))

    # Main loop (This is the actual game part):
    while gameRunning:
        print(f"Turn: {turnCount}")

        for i in range(len(playerList)):  # For each player
            turnFinished = False
            playerList[i].setIsRollingDone(False)  # Reset dice rolls at the start of each players turn

            while not turnFinished:  # Loop until the end turn button is pressed
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:  # Close pygame if the X is clicked
                        gameRunning = False
                        pygame.quit()
                        exit()

                screen.blit(main_surface, (0, 0))  # Displays the board

                playerList[i].displayNameMoney(screen, font, PLAYER_COLS[i], (width, height), i)  # Display the current player and how much money they have

                # Rolling
                if playerList[i].getIsRollingDone() == False and playerList[i].getIsAI() == False: # If the player can roll not an AI
                    if rollButton.draw(screen):  # Draw a button players can press to roll
                        playerList[i].move(board, playerList, screen, font, PLAYER_COLS[i])

                elif playerList[i].getIsAI() == True:  # If the player is AI, have them roll until they can't and end thier turn
                    playerList[i].move(board, playerList, screen, font, PLAYER_COLS[i])

                    if playerList[i].getIsRollingDone() == True:  # This means that an AI player will always roll again if they get doubles 
                        turnFinished = True

                if playerList[i].getIsRollingDone() == True or playerList[i].getDoubleRolls() != 0:  # These condtions mean player has rolled at least once this turn
                    rollDisplay(screen, PLAYER_COLS[i], (width, height), playerList[i])  # Displays the dice the player rolled

                # Update display to show current board state
                for j in range(len(playerList)):  
                    playerList[j].displayProperties(screen, PLAYER_COLS[j], j, PROPERTY_LOCATIONS)  # Display who ownes which property
                    playerList[j].showLocation(screen, PIECE_IMAGES, PLAYER_LOCATIONS, playerList[j].piece)  # Display all of the players pieces on the board

                if playerList[i].getIsAI() == False:  # Don't draw the button for AI players
                    if endTurnButton.draw(screen):  # Button to pass the turn
                        turnFinished = True

                pygame.display.update()
                clock.tick(60)

                # If the current player is AI, hang after thier turn for a couple seconds so everyone else can see what they did
                if playerList[i].getIsAI() == True:
                    time.sleep(2)

        turnCount += 1

if __name__ == "__main__":
    main()
