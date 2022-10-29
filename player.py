import tile
import random
from typing import List
from datetime import datetime

import pygame
from draw import Button, draw_text

random.seed(datetime.now().timestamp())

jailIndex = 10


class Player:
    def __init__(self, pieceIn: int, AI: bool):
        self.money: int = 1500  # The amount of money the player currently has
        self.properties: list[tile.Property] = []  # properties play owns
        self.location: int = 0  # Index value for the tile the player is currently
        self.getOutOfJailCards: int = (
            0  # The number of get out of jail free cards the player currently has
        )
        self.isInJail: bool = False  # Is the player currently in jail
        self.isRollingDone: bool = False  # Set to true once the player can no longer roll during thier current turn
        self.doubleRolls: int = 0  # Increases whenever the player rolls doubles, set back to zero when they don't
        self.piece: int = pieceIn  # Index of the players piece
        self.isBankrupt: bool = False  # Is the player currently bankrupt
        self.isAI: bool = AI

    # For testing purposes
    # def __init__(
    #     self, pieceIn: int, AI: bool, properties: list[tile.Property], location: int
    # ):
    #     self.money: int = 1500  # The amount of money the player currently has
    #     self.properties: list[tile.Property] = properties  # properties play owns
    #     self.location: int = (
    #         location  # Index value for the tile the player is currently
    #     )
    #     self.getOutOfJailCards: int = (
    #         0  # The number of get out of jail free cards the player currently has
    #     )
    #     self.isInJail: bool = False  # Is the player currently in jail
    #     self.doubleRolls: int = 0  # Increases whenever the player rolls doubles, set back to zero when they don't
    #     self.piece: int = pieceIn  # Index of the players piece
    #     self.isBankrupt: bool = False  # Is the player currently bankrupt
    #     self.isAI: bool = AI

    # Test function to print all the properties a player owns
    def getProperties(self) -> str:
        propList = ""
        for prop in self.properties:
            propList += f"{prop.getIndex()}, "

        return propList

    # pay another player
    def pay(self, landedOn: tile.Property, playerList) -> None:
        cost = (
            landedOn.getRent()
        )  # wherever we get cost, varies based on propery and houses / hotels
        if self.money >= cost:
            self.money -= cost
            playerList[landedOn.getOwner()].money += cost
        else:  # if we don't have enough just give them all we have and are noe bankrupt
            playerList[landedOn.getOwner()].money += self.money
            self.money -= cost
            self.isBankrupt = True
            self.RemoveProperties()

    # Get or pay money to the bank, amount can be positive or negative, with
    # negative meaning loss of money and positive meaning gain.
    def bankTransaction(self, amount: int) -> None:
        if self.money + amount > 0:
            self.money += amount
        else:  # If we don't have enough money to pay, we lost all we have and are bankrupt
            self.money = 0
            self.isBankrupt = True
            self.RemoveProperties()

    # Simulate dice roll, two random numbers 1-6, returns the rolled values in a list
    # TODO Fix what changing this function call probably broke in jail
    def roll(self, screen: pygame.surface.Surface) -> List[int]:
        diceOne = random.randint(1, 6)
        diceTwo = random.randint(1, 6)

        # TODO Popup showing what the dice rolls where
        print("Rolled: " + str(diceOne) + " & " + str(diceTwo))  # High quality viusal interface
        # width, height = main_surface.get_height(), main_surface.get_width()

        # We need all the dice in a list so we can index them
        # All numbers are random placeholders atm
        '''diceImageList = []
        diceImageList.append(pygame.image.load("Images/dice1.png"))
        diceImageList.append(pygame.image.load("Images/dice2.png"))
        diceImageList.append(pygame.image.load("Images/dice3.png"))
        diceImageList.append(pygame.image.load("Images/dice4.png"))
        diceImageList.append(pygame.image.load("Images/dice5.png"))
        diceImageList.append(pygame.image.load("Images/dice6.png"))

        rollWindowOpen = True

        while rollWindowOpen:
            screen.blit(diceImageList[diceOne - 1], (0, 0))  # Draw the two dice
            screen.blit(diceImageList[diceTwo - 1], (20, 20))

            closeImage = pygame.image.load("Images/closeButton.png")
            closeButton = Button(500, 500, closeImage, (200, 50))

            if closeButton.draw(screen):
                rollWindowOpen = False'''



        return [diceOne, diceTwo]

    # move a given distance
    def move(
        self,
        board: List[tile.Tile],
        playerList,
        screen: pygame.surface.Surface,
        font: pygame.font.Font,
        text_color: tuple[int, int, int],
    ):
        print(self.location)
        dice = self.roll(screen)
        if self.isInJail:
            # TODO Once we have pygame figured out, we need an option to pay $50 to leave jail early
            # TODO If a player has a get out of jail free card, they can use it to get out of jail
            self.escapeJail(dice)
            return

        if dice[0] != dice[1]:  # If we didn't roll doubles
            self.isRollingDone = True
            self.doubleRolls = 0

        else:  # We did roll doubles
            self.doubleRolls += 1

        if self.doubleRolls == 3:  # Our third double roll takes us immediatly to jail
            self.isRollingDone = True
            self.doubleRolls = 0
            self.toJail()

        distance = dice[0] + dice[1]
        moved = 0
        while moved < distance:
            self.location = self.location + 1
            if self.location >= len(board):
                print(f"Player {self.piece} passed Go!")
                self.location = 0
                self.bankTransaction(200)
            moved += 1

        if isinstance(board[self.location], tile.Property):
            effect = board[self.location].landedOn(self.piece)
        else:
            effect = board[self.location].landedOn()

        self.landOnParse(effect, board, playerList, screen, font, text_color)
        # TODO: Remove test print
        print(f"player {self.piece} has reached space {self.location}")

    def landOnParse(
        self,
        effect: str,
        board: list[tile.Tile],
        playerList,
        screen: pygame.surface.Surface,
        font: pygame.font.Font,
        text_color: tuple[int, int, int],
    ) -> None:
        instructions = effect.split(":")
        print(f"{effect=}")
        if len(instructions) > 1:
            instructionValue: int = int(
                instructions[1]
            )  # This value will either be a dollar amount or a tile index depending on the contex

        match instructions[0]:
            case "Charge":
                self.bankTransaction(
                    -instructionValue
                )  # instructionValue is a dollar amount

            case "ReceiveFromAll":  # All other players give you money
                # instructionValue is a dollar amount owed in this context
                for player in playerList:
                    if player.piece != self.piece:
                        if (
                            player.money < instructionValue
                        ):  # Player can't afford, they go bankrupt
                            self.money += player.money  # Give money the player has
                            player.money = 0
                            player.isBankrupt = True
                            self.RemoveProperties()
                        else:  # Players can afford to pay
                            self.money += instructionValue  # You get money
                            player.money -= instructionValue  # They lose the money

            case "Pay":  # board[instructionValue] should be the inedex value of the property being landed on
                self.pay(board[instructionValue], playerList)

            case "PayRailroad":
                totalCost = board[
                    instructionValue
                ].getRent()  # instructionValue is a tile index here
                railroadAmt = 0
                for prop in playerList[board[instructionValue].getOwner()].properties:
                    if prop.getColor() == "Railroad":
                        railroadAmt += 1

                for i in range(1, railroadAmt):
                    totalCost *= 2

                if totalCost >= self.money:  # Can't affor rent, bankrupt
                    playerList[board[instructionValue].getOwner()].money += self.money
                    self.money = 0
                    self.isBankrupt = True
                    self.RemoveProperties()

                else:
                    playerList[board[instructionValue].getOwner()].money += totalCost
                    self.money -= totalCost

            case "PayUtility":  # Utility indexes are 12 and 28
                amountDue = random.randint(1, 6)  # Roll a dice

                if (
                    board[12].getOwner() == board[28].getOwner()
                ):  # If the same player ownes both utilities
                    amountDue *= 10

                else:  # Player only owns one utility
                    amountDue *= 4

                if amountDue >= self.money:  # Can't afford rent, bankrupt
                    playerList[
                        board[instructionValue].getOwner()
                    ].money += self.money  # Give player all we have left
                    self.money = 0
                    self.isBankrupt = True
                    self.RemoveProperties()  # All owned properties return to the bank

                else:  # Pay rent calculated above
                    playerList[board[instructionValue].getOwner()].money += amountDue
                    self.money -= amountDue

            case "PayAll":  # You give all other players money
                for player in playerList:
                    if player.piece != self.piece:
                        if self.money >= instructionValue:
                            player.money += instructionValue
                            self.money -= instructionValue
                        else:
                            player.money += self.money
                            self.money = 0

                        if self.money == 0:
                            self.isBankrupt = True
                            break

            case "Purchase":  # Note that instruction here reffers to the inedex of the tile being purchased
                purchaseProperty = True
                if not self.isAI:
                    decisionMade = False

                    yes = pygame.images.load("Images/yes.png")
                    no = pygame.images.load("Images/no.png")

                    while not decisionMade:
                        draw_text(
                            screen,
                            f"Do you want to purchase this property?",
                            font,
                            text_color,
                            10,
                            10,
                        )

                        # TODO: Get pictures of a 'Yes' or 'No.'
                        yesButton = Button(50, 100, yes, (20, 20))
                        noButton = Button(100, 100, no, (20, 20))

                        if not decisionMade:
                            if yesButton.draw(screen):
                                decisionMade = True
                                purchaseProperty = True
                                # Player buys property here.

                            # Player does not buy property, the screen closes.
                            elif noButton.draw(screen):
                                decisionMade = True
                                purchaseProperty = False

                if purchaseProperty:
                    if (
                        board[instructionValue].getCost() < self.money
                    ):  # Force buy property if you can afford it
                        self.money -= board[
                            instructionValue
                        ].getCost()  # TODO Make purchasing optional
                        self.properties.append(board[instructionValue])
                        board[instructionValue].setOwner(self.piece)
                    else:
                        print("Can't afford property!")

            case "Move":
                if instructionValue < 0:
                    for i in range(-instructionValue):
                        self.location -= 1
                        if self.location < 0:
                            self.location = len(board) - 1
                else:
                    for i in range(instructionValue):
                        self.location += 1
                        if self.location >= len(board):
                            self.location = 0
                            self.bankTransaction(200)

            case "ToJail":
                self.toJail()

            case "GetOutCard":
                self.getOutOfJailCards += 1

            case "toRailroad":
                railroadLocs = [5, 15, 25, 35]
                currClosestLoc = len(board)
                for loc in railroadLocs:
                    if self.location - loc <= currClosestLoc:
                        currClosestLoc = loc

                self.location = currClosestLoc

            case "MoveAll":
                for player in playerList:
                    # Copied from the 'Move' case above
                    if instructionValue < 0:
                        for i in range(-instructionValue):
                            player.location -= 1
                            if player.location < 0:
                                player.location = len(board) - 1
                    else:
                        for i in range(instructionValue):
                            player.location += 1
                            if player.location >= len(board):
                                player.location = 0
                                player.bankTransaction(200)

    def escapeJail(self, dice: List[int]) -> None:
        if dice[0] == dice[1]:
            self.isInJail = False

        self.isRollingDone = True  # One roll per turn in jail, regardless of if you roll doubles and get out or not

    def RemoveProperties(
        self,
    ) -> None:  # Called when a player goes bankrupt, returns all of thier properties to the bank
        for OwnedItem in self.properties:
            OwnedItem.owner = None
        self.properties = []

    def toJail(self) -> None:
        self.index = jailIndex
        self.isInJail = True

    def displayNameMoney(
        self,
        screen: pygame.surface.Surface,
        font: pygame.font.Font,
        text_color: tuple[int, int, int],
        screen_size: tuple[int, int],
        player_index: int,
    ) -> None:
        # Positions
        money_position: tuple[float, float] = (
            screen_size[0] / 7,
            screen_size[1] / 1.36,
        )

        player_position: tuple[float, float] = (screen_size[1] / 3, screen_size[0] / 7)

        # Display
        draw_text(
            screen,
            f"Money: ${self.money}",
            font,
            text_color,
            money_position[0],
            money_position[1],
        )
        draw_text(
            screen,
            f"Player {player_index + 1}'s turn",
            font,
            text_color,
            player_position[0],
            player_position[1],
        )
        # screen.blit(
        #     font.render(f"Money: ${self.money}", True, text_color), money_position
        # )
        # screen.blit(
        # font.render(f"Player {player_index + 1}'s turn", True, text_color),
        # player_position,
        # )

    # Purpose: To display player name, properties, money, etc.
    def displayProperties(
        self,
        screen: pygame.surface.Surface,
        text_color: tuple[int, int, int],
        player_index: int,
        property_locations: list[tuple[int, int]],
    ) -> None:

        number_font: pygame.font.Font = pygame.font.SysFont("arialblack", 20)

        for property in self.properties:
            location: tuple[int, int] = property_locations[property.index]

            pygame.draw.circle(screen, text_color, location, 20)

            number: pygame.surface.Surface = number_font.render(
                f"{player_index + 1}", True, (0, 0, 0)
            )
            text_location: list[int] = [location[0] - 6, location[1] - 15]

            if 20 > property.index > 9:
                number = pygame.transform.rotate(number, -90)
                text_location[0] -= 6
                text_location[1] += 8
            elif 30 > property.index >= 20:
                number = pygame.transform.rotate(number, 180)
                text_location[0] += 1
                text_location[1] += 2
            elif property.index >= 30:
                number = pygame.transform.rotate(number, 90)
                text_location[0] -= 8
                text_location[1] += 9

            screen.blit(
                number,
                text_location,
            )

    def showLocation(
        self,
        screen: pygame.surface.Surface,
        pieces: list[pygame.surface.Surface],
        player_locations: list[list[tuple[int, int]]],
        index: int,
    ) -> None:
        scaledImages: list[pygame.surface.Surface] = []

        # print(self.location)

        for piece in pieces:
            scaledImages.append(pygame.transform.scale(piece, (40, 40)))

        rotatedImage: pygame.surface.Surface = scaledImages[index]

        if 20 > self.location > 9:
            rotatedImage = pygame.transform.rotate(scaledImages[index], -90)
        elif 30 > self.location >= 20:
            rotatedImage = pygame.transform.rotate(scaledImages[index], 180)
        elif self.location >= 30:
            rotatedImage = pygame.transform.rotate(scaledImages[index], 90)

        if self.isInJail:
            if index == 0:
                screen.blit(
                    rotatedImage,
                    (
                        player_locations[self.location][index][0] + 45,
                        player_locations[self.location][index][1],
                    ),
                )
            elif index == 1:
                screen.blit(
                    rotatedImage,
                    (
                        player_locations[self.location][index][0] + 90,
                        player_locations[self.location][index][1] - 60,
                    ),
                )
            elif index == 2 or index == 3:
                screen.blit(
                    rotatedImage,
                    (
                        player_locations[self.location][index][0],
                        player_locations[self.location][index][1] - 40,
                    ),
                )
        else:
            screen.blit(
                rotatedImage,
                (
                    player_locations[self.location][index][0],
                    player_locations[self.location][index][1],
                ),
            )

    def getIsRollingDone(self) -> bool:  # Return if player can roll at the current moment
        return self.isRollingDone

    def setIsRollingDone(self, value) -> None:  # Set player rolling ability to passed value
        self.isRollingDone = value
