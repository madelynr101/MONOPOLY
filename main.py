# from xml.dom.minidom import TypeInfo
from turtle import width
import pygame
from sys import exit
from draw import Button, draw_text

# Import backend functions for components of the game.
import tile
import player


# Initialize pygame so we can initialize font
pygame.init()

# Default font
font: pygame.font.Font = pygame.font.SysFont("arialblack", 40)

# Default text color
TEXT_COL: tuple[int, int, int] = (0, 0, 0)
PLAYER_COLS: list[tuple[int, int, int]] = [
    (224, 49, 22),
    (42, 176, 12),
    (40, 48, 209),
    (209, 155, 46),
]

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
def choose_people(screen, player_type, amnt_players, players, fillerList, AI_person, person_type):
    # whether a person has picked how many players they want, AI or human 
    chosen = False 

    # images for player selection:
    zero = pygame.image.load("Images/0.png")
    one = pygame.image.load("Images/1.png")
    two = pygame.image.load("Images/2.png")
    three = pygame.image.load("Images/3.png")
    four = pygame.image.load("Images/4.png")

    zeroButton = Button(150, 500, zero, (80, 80))
    oneButton = Button(350, 500, one, (80, 80))
    twoButton = Button(550, 500, two, (80, 80))
    threeButton = Button(750, 500, three, (80, 80))
    fourButton = Button(950, 500, four, (80, 80))
    buttons = [zeroButton, oneButton, twoButton, threeButton, fourButton]

    # Choose amount of AI players:
    while chosen != True:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
                pygame.quit()
                quit()

        draw_text(
            screen,
            f"How many {person_type} players do you want 0-4?",
            font,
            TEXT_COL,
            20,
            20,
        )

        # player buttons output to screen and data collected
        for i in range(len(buttons)):
            buttons[i].draw(screen)
            if buttons[i].clicked:
                player_type = i
                chosen = True
                
        if chosen:
            print(player_type)
            break

        pygame.display.update()


# Matt Chenot
# Purpose: To display dice roll screen and the dice after the roll
def roll():
    # A roll button on the main bit that players press to roll
    # Doing this brings up a pop up with that shows the faces of the two dice they rolled
    # There is then a button to close this screen

    # NOTE: think on moving this to the roll function, that way the popup can show up for the jail stuff to

    dice1 = pygame.images.load("Images/dice1.png")
    dice2 = pygame.images.load("Images/dice2.png")
    dice3 = pygame.images.load("Images/dice3.png")
    dice4 = pygame.images.load("Images/dice4.png")
    dice5 = pygame.images.load("Images/dice5.png")
    dice6 = pygame.images.load("Images/dice6.png")

    pass


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
def jail(prisoner: int):
    choiceMade = False
    escapeImage = pygame.images.load("Images/escapeButton.png")
    payImage = pygame.images.load("Images/payButton.png")
    useCardImage = pygame.images.load("Images/cardButton.png")
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
# Purpose: To choose the character for each person, either human or AI.
def player_loop(
    screen: pygame.surface.Surface, playerList: list[player.Player], playersChosen
):
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
    chosen = True
    jailIndex = 10

    # bank instantiation

    # put tiles in this array:
    board = []

    load_tiles(board)

    # player array:
    playerList: list[player.Player] = []

    # get how many players
    players = 4

    turnCount = 1

    # For testing purposes
    # playerProperties: list[list[tile.Property]] = [
    #     [board[1], board[5], board[13], board[23], board[34]],
    #     [board[3], board[15], board[21], board[32]],
    #     [board[6], board[11], board[24], board[31]],
    #     [board[8], board[18], board[26], board[37]],
    # ]

    # change when giving players piece selection if we do that
    for i in range(players):
        # For testing purposes
        # playerList.append(player.Player(i, True, playerProperties[i], 39))
        playerList.append(
            player.Player(i, True)
        )  # Create a player in the list, just incrementing the piece they are

    # for i in range(len(board)):
    #  screen.blit(tileSurface, (00, 100 * i))

    # amount of human vs AI players playing
    AI_person = False
    fillerList = []
    person_type = ""
    AI_player = 0 
    human_player = 0 

    amnt_players = human_player + AI_player

    AI_player = choose_people(
        screen, AI_player, amnt_players, players, fillerList, AI_person, person_type = "AI"
    )

    human_player = choose_people(
        screen, human_player, amnt_players, players, fillerList, AI_person, person_type = "human"
    )

    

    playersChosen = 0
    # if playersChosen < players:
    #   player_loop(screen, playerList, playersChosen)

    endTurnImage = pygame.image.load("Images/endTurn.png")
    endTurnButton = Button(width / 7, height / 1.26, endTurnImage, (200, 50))

    rollImage = pygame.image.load("Images/rollButton.png")
    rollButton = Button(width / 2.75, height / 1.26, rollImage, (200, 50))

    # Main loop:
    while gameRunning:
        # TESTING LOOP
        # Quits the game whenever the application window has been closed.

        print(f"Turn: {turnCount}")

        for i in range(len(playerList)):
            turnFinished = False
            playerList[i].setIsRollingDone(False)  # Reset dice rolls at the start of each players turn

            while not turnFinished:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        gameRunning = False
                        pygame.quit()
                        exit()

                screen.blit(main_surface, (0, 0))

                playerList[i].displayNameMoney(
                    screen, font, PLAYER_COLS[i], (width, height), i
                )

                for j in range(len(playerList)):
                    playerList[j].displayProperties(
                        screen,
                        PLAYER_COLS[j],
                        j,
                        PROPERTY_LOCATIONS,
                    )

                    playerList[j].showLocation(
                        screen, PIECE_IMAGES, PLAYER_LOCATIONS, j
                    )

                if endTurnButton.draw(screen):  # Button to pass the turn
                    turnFinished = True

                # A test that actually does what it's suppost to for once
                # closeImage = pygame.image.load("Images/closeButton.png")
                # closeButton = Button(500, 500, closeImage, (200, 50))
                # if closeButton.draw(screen):
                    # pass

                # Rolling
                if playerList[i].getIsRollingDone() == False: # If the player can roll
                    if rollButton.draw(screen):  
                        playerList[i].move(board, playerList, screen, font, PLAYER_COLS[i])  # The visuals for the dice are done in the roll function since that is also called during jail stuff

                pygame.display.update()
                clock.tick(60)
        turnCount += 1


if __name__ == "__main__":
    main()
