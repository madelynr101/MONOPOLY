import tile
import random
from typing import List
from dataclasses import dataclass

import pygame
from draw import draw_text

jailIndex = 10

@dataclass
class flavor:
    text: str
    amount: int

class Player:
    def __init__(self, pieceIn: int, AI: bool):
        self.money: int = 1500  # The amount of money the player currently has
        self.properties: list[tile.Property] = []  # properties play owns
        self.location: int = 0  # Index value for the tile the player is currently
        self.getOutOfJailCards: int = 0  # The number of get out of jail free cards the player currently has
        self.turnsInJail: int = 0;  # Turns in jail, players automatically get out after three turns
        self.isInJail: bool = False  # Is the player currently in jail
        self.isRollingDone: bool = False  # Set to true once the player can no longer roll during thier current turn
        self.doubleRolls: int = 0  # Increases whenever the player rolls doubles, set back to zero when they don't
        self.lastRoll: tuple[int, int] = []  # The values of the players last roll, used to draw the dice on screen
        self.piece: int = pieceIn  # Index of the players piece
        self.isBankrupt: bool = False  # Is the player currently bankrupt
        self.isAI: bool = AI
        self.choosingProperty: bool = False
        self.jailChoiceMade: bool = False
        self.acknowledgingTax: bool = False
        self.acknowledgingChance: bool = False
        self.acknowledgingCommunity: bool = False
        self.flavorText: str = ""
        self.cardAmount: int = 0
        self.isPaying: bool = False
        self.isPayed: bool = False

    # Test function to print all the properties a player owns
    def getProperties(self) -> str:
        propList: str = ""
        for prop in self.properties:
            propList += f"{prop.getIndex()}, "

        return propList

    # Pay another player
    def pay(self, landedOn: tile.Property, playerList) -> None:
        cost: int = landedOn.getRent()  # wherever we get cost, varies based on propery and houses / hotels

        # If player can afford the price
        if self.money >= cost:
            self.money -= cost
            playerList[landedOn.getOwner()].money += cost

        # If player can't afford the price, pay what they have and are now bankrupt
        else:
            playerList[landedOn.getOwner()].money += self.money
            self.money -= cost
            self.isBankrupt = True
            self.RemoveProperties()

    # Get or pay money to the bank, amount can be positive or negative
    def bankTransaction(self, amount: int) -> None:
        if self.money + amount > 0:
            self.money += amount

        # Else we don't have enough to pay the bank
        else:
            self.money = 0
            self.isBankrupt = True
            self.RemoveProperties()

    # Simulate dice roll, two random numbers 1-6, returns the rolled values in a list
    def roll(self) -> tuple[int, int]:
        diceOne: int = random.randint(1, 6)
        diceTwo: int = random.randint(1, 6)
        self.lastRoll: tuple[int, int] = [diceOne, diceTwo]  # Needed to display the correct dice elsewhere
        return [1, 1]  # Very important NOTE: Don't forget to remove this line
        return [diceOne, diceTwo]

    # Does player movment, rolls dice, then moves to requisite number of spaces
    def move(
        self,
        board: List[tile.Tile],
        playerList
    ) -> None:
        print(self.location)
        dice: tuple[int, int] = self.roll()

        # Rolling has a completly diffrent context in jail, hanled in escapeJail()
        if self.isInJail:
            self.escapeJail(dice)
            return  # End movement

        # If player didn't roll doubles
        if dice[0] != dice[1]:
            self.isRollingDone = True
            self.doubleRolls = 0

        # Player did roll doubles
        else:
            self.doubleRolls += 1

        # Third double roll takes player immediatly to jail
        if self.doubleRolls == 3:
            self.isRollingDone = True
            self.doubleRolls = 0
            self.toJail()
            return # end movment

        distance: int = dice[0] + dice[1]  # This is the number of spaces we are gonna move
        moved: int = 0  # How many spaces we have moved

        # The actual movment
        while moved < distance:
            self.location = self.location + 1
            if self.location >= len(board):  # $200 for passing go
                print(f"Player {self.piece} passed Go!")
                self.location = 0
                self.bankTransaction(200)
            moved += 1

        # Effects of space landed on
        if isinstance(board[self.location], tile.Property):
            effect: str = board[self.location].landedOn(self.piece)
        elif isinstance(board[self.location], tile.Chance):
            if not self.isAI:
                self.acknowledgingChance = True
            flavorInfo: flavor = flavor("", 0)
            effect: str = board[self.location].landedOn(flavorInfo)
            self.flavorText = flavorInfo.text
            self.cardAmount = flavorInfo.amount
        elif isinstance(board[self.location], tile.CommunityChest):
            if not self.isAI:
                self.acknowledgingCommunity = True
            flavorInfo: flavor = flavor("", 0)
            effect: str = board[self.location].landedOn(flavorInfo)
            self.flavorText = flavorInfo.text
            self.cardAmount = flavorInfo.amount
        else:
            if isinstance(board[self.location], tile.IncomeTax) or isinstance(board[self.location], tile.LuxuryTax):
                if not self.isAI:
                    self.acknowledgingTax = True

            effect: str = board[self.location].landedOn()

        self.landOnParse(effect, board, playerList)


    # Spaces return a formated string regarding what they do, this function parses those strings and preforms the desired action
    # Strings are of the format 'Action:Value'
    # The action is required and is the effect of the space
    # The ':Value' is optional, Value is some integer value that to specificy something about the action (i.e. the amount of rent to pay)
    def landOnParse(
        self,
        effect: str,
        board: list[tile.Tile],
        playerList,
    ) -> None:
        instructions = effect.split(":")
        print(f"{effect=}")

        if len(instructions) > 1:  # If there is an integer value, store it in instructionValue
            instructionValue: int = int(
                instructions[1]
            )  # This value will either be a dollar amount or a tile index depending on the contex

        match instructions[0]:
            # You give the bank money
            case "Charge":
                self.bankTransaction(
                    -instructionValue
                )  # instructionValue is a dollar amount

            # All other players give you money
            case "ReceiveFromAll":
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

            # Pay the owner of the property you landed on the required rent for that space
            case "Pay":  # board[instructionValue] should be the inedex value of the property being landed on
                self.pay(board[instructionValue], playerList)

            # Special case for paying rent for railroads
            case "PayRailroad":
                totalCost = board[instructionValue].getRent()  # instructionValue is a tile index here
                railroadAmt = 0  # Number of railroads player owned

                for prop in playerList[board[instructionValue].getOwner()].properties:
                    if prop.getColor() == "Railroad":
                        railroadAmt += 1

                # Double rent owed for each railroad owned
                for _ in range(1, railroadAmt):
                    totalCost *= 2

                # Can't afford rent, bankrupt
                if totalCost >= self.money:
                    playerList[board[instructionValue].getOwner()].money += self.money
                    self.money = 0
                    self.isBankrupt = True
                    self.RemoveProperties()

                # Pay rent
                else:
                    playerList[board[instructionValue].getOwner()].money += totalCost
                    self.money -= totalCost

            # Special case for paying rent for utilities
            case "PayUtility":  # Utility indexes are 12 and 28
                amountDue: int = 0

                # If the same player ownes both utilities
                if board[12].getOwner() == board[28].getOwner():
                    amountDue = (self.lastRoll[0] + self.lastRoll[1]) *  10

                # Player only owns one utility
                else:
                    amountDue = (self.lastRoll[0] + self.lastRoll[1]) * 4

                # Can't afford rent, bankrupt
                if amountDue >= self.money:
                    playerList[board[instructionValue].getOwner()].money += self.money  # Give player all we have left
                    self.money = 0
                    self.isBankrupt = True
                    self.RemoveProperties()  # All owned properties return to the bank

                # Pay rent calculated above
                else:
                    playerList[board[instructionValue].getOwner()].money += amountDue
                    self.money -= amountDue

            # You give all other players money
            case "PayAll":
                for player in playerList:
                    if player.piece != self.piece:
                        if self.money >= instructionValue:  # Player can afford to pay
                            player.money += instructionValue
                            self.money -= instructionValue

                        # Player can't afford, bankrupt
                        else:
                            self.money <= 0
                            self.isBankrupt = True
                            self.RemoveProperties()  # All owned properties return to the bank
                            break

            # Purchase the unowned property at given index
            case "Purchase":  # Note that instruction here reffers to the index of the tile being purchased
                if not self.isAI:  # Players can chose wheather to buy property or not
                    self.choosingProperty = True
                else:  # This is what the AI does, always buy if you have the money
                    if board[instructionValue].getCost() < self.money:  # Force buy property if AI can afford it
                        self.money -= board[instructionValue].getCost()
                        self.properties.append(board[instructionValue])
                        board[instructionValue].setOwner(self.piece)

            # Move number of spaces
            case "Move":
                if instructionValue < 0:  # Move backwards (no money from passing go)
                    for i in range(-instructionValue):
                        self.location -= 1
                        if self.location < 0:
                            self.location = len(board) - 1

                else:  # Move forwards
                    for i in range(instructionValue):
                        self.location += 1
                        if self.location >= len(board):
                            self.location = 0
                            self.bankTransaction(200)  # $200 for passing go

            # Go to jail
            case "ToJail":
                self.toJail()

            # Card effect: recieve a get out of jail free card
            case "GetOutCard":
                self.getOutOfJailCards += 1

            # Card effect: move to the nearest railraod
            case "ToRailroad":
                railroadLocs: list[int] = [5, 15, 25, 35]
                currClosestLoc: int = len(board)

                for loc in railroadLocs:
                    if self.location - loc <= currClosestLoc:
                        currClosestLoc = loc

                self.location = currClosestLoc

            # Card effect: move all players some number of spaces
            case "MoveAll":
                for player in playerList:
                    if instructionValue < 0:  # Move backwards (no money from passing go)
                        for i in range(-instructionValue):
                            player.location -= 1
                            if player.location < 0:  # Loop back to end of board
                                player.location = len(board) - 1

                    else:   # Move forwards
                        for i in range(instructionValue):
                            player.location += 1
                            if player.location >= len(board):  # $200 for passing go
                                player.location = 0
                                player.bankTransaction(200)

    # Seeing the player is able to leave jail this turn
    def escapeJail(self, dice: tuple[int, int]) -> None:
        if dice[0] == dice[1]:
            self.isInJail = False
            self.turnsInJail = 0

        self.turnsInJail += 1  # Increment at the end of each turn in jail

        if self.turnsInJail > 3:  # Automatically leave jail after third turn if you are still in
            self.isInJail = False
            self.turnsInJail = 0

        self.isRollingDone = True  # One roll per turn in jail, regardless of if you roll doubles and get out or not

    # Called when a player goes bankrupt, returns all of thier properties to the bank
    def RemoveProperties(self) -> None:
        for OwnedItem in self.properties:
            OwnedItem.owner = None
        self.properties = []

    # Player is sent to jail
    def toJail(self) -> None:
        self.isRollingDone = True
        self.location = jailIndex
        self.isInJail = True

    # Diplay info about who current player is and how much money they have
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

    def AIJailDecision(self) -> None:
        self.jailChoiceMade = True

        if(self.getOutOfJailCards > 0):
            self.getOutOfJailCards -= 1
            self.isInJail = False
            self.move()

        elif(self.money > 50):
            self.bankTransaction(-50)
            self.isInJail = False
            self.turnsInJail = 0
            self.move()

        else:
            self.move()

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

            # Rotate the property markers to match the boards orientation if needed
            if 20 > property.index > 9:  # Left side of borad
                number = pygame.transform.rotate(number, -90)
                text_location[0] -= 6
                text_location[1] += 8

            elif 30 > property.index >= 20:  # Top of board
                number = pygame.transform.rotate(number, 180)
                text_location[0] += 1
                text_location[1] += 2

            elif property.index >= 30:  # Right side of board
                number = pygame.transform.rotate(number, 90)
                text_location[0] -= 8
                text_location[1] += 9

            screen.blit(
                number,
                text_location,
            )

    # Draws the player icons at thier current locations on the board
    def showLocation(
        self,
        screen: pygame.surface.Surface,
        pieces: list[pygame.surface.Surface],
        player_locations: list[list[tuple[int, int]]],
        index: int,
    ) -> None:
        if self.isBankrupt:
            return

        scaledImages: list[pygame.surface.Surface] = []

        # Scale the pieces down so they can all fit on one square
        for piece in pieces:
            scaledImages.append(pygame.transform.scale(piece, (40, 40)))

        rotatedImage: pygame.surface.Surface = scaledImages[index]

        # Rotate the player markers to match the boards orientation if needed
        if 20 > self.location > 9:  # Left side of borad
            rotatedImage = pygame.transform.rotate(scaledImages[index], -90)

        elif 30 > self.location >= 20:  # Top of board
            rotatedImage = pygame.transform.rotate(scaledImages[index], 180)

        elif self.location >= 30:  # Right side of board
            rotatedImage = pygame.transform.rotate(scaledImages[index], 90)

        if self.isInJail:
            if index == 0:  # Index is the current player, so this is player 1
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

    # Return if player can roll at the current moment
    def getIsRollingDone(self) -> bool:
        return self.isRollingDone

    # Returns if a player is AI
    def getIsAI(self) -> bool:
        return self.isAI

    # Returns if a player is bankrupt
    def getIsBankrupt(self) -> bool:
        return self.isBankrupt

    # Returns if a player is in jail
    def getIsInJail(self) -> bool:
        return self.isInJail

    # Return # of times player has rolled dobules this turn
    def getDoubleRolls(self) -> int:
        return self.doubleRolls

    # Return the players last roll
    def getLastRoll(self) -> tuple[int, int]:
        return self.lastRoll

    # Set player rolling ability to passed value
    def setIsRollingDone(self, value: bool) -> None:
        self.isRollingDone = value

    # Set if player is AI to passed value
    def setIsAI(self, value: bool) -> None:
        self.isAI = value

    def getChoosingProperty(self) -> bool:
        return self.choosingProperty

    def setChoosingProperty(self, value: bool) -> None:
        self.choosingProperty = value

    def getJailChoiceMade(self) -> bool:
        return self.jailChoiceMade

    def setJailChoiceMade(self, value: bool) -> None:
        self.jailChoiceMade = value

    def getAcknowledgingChance(self) -> bool:
        return self.acknowledgingChance

    def setAcknowledgingChance(self, value: bool) -> None:
        self.acknowledgingChance = value

    def getAcknowledgingCommunity(self) -> bool:
        return self.acknowledgingCommunity

    def setAcknowledgingCommunity(self, value: bool) -> None:
        self.acknowledgingCommunity = value

    def getFlavorText(self) -> str:
        return self.flavorText

    def setFlavorText(self, text: str) -> None:
        self.flavorText = text
    
    def getCardAmount(self) -> int:
        return self.cardAmount

    def setCardAmount(self, amount: int) -> None:
        self.cardAmount = amount

    def getAcknowledgingTax(self) -> bool:
        return self.acknowledgingTax

    def setAcknowledgingTax(self, value: bool) -> None:
        self.acknowledgingTax = value
