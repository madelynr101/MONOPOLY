from abc import ABCMeta, abstractmethod
import card
import cardTypes

import pygame
from draw import Button, draw_text

# This is the main abstract tile class
# All the other types of tiles inherit and build thier own functionality of this class
class Tile(metaclass=ABCMeta):
    def __init__(self, index) -> None:
        self.index = index

    @abstractmethod
    # Landed on functions return a formated string specify what that specific tile is supposed to do
    def landedOn(self) -> str:
        pass

    def getIndex(self) -> int:
        return self.index


# The main property class, includes regular properties, railroads and utilities
class Property(Tile):
    def __init__(self, index):
        super().__init__(index)
        self.owner: int = None
        self.cost: int = 0
        self.rent: int = 0
        self.color: str = None

    # Parameterized constructor
    def __init__(self, index: int, cost: int, rent: int, color: str):
        super().__init__(index)
        self.owner = None
        self.cost = cost
        self.rent = rent
        self.color = color  # Note that this value is also used to specifiy if the property is a railroad or a utility

    def landedOn(self, landingPlayer: int) -> str:
        instructionToReturn: str = ""

        if self.owner == None:  # If no one owns this property
            instructionToReturn = f"Purchase:{self.index}"  # Player class will handle having enough money / if they want to but it

        # If property is owned, but not by current player (landing player owning property does nothing)
        elif self.owner != landingPlayer:
            if self.color == "Railroad":  # Rent increases for each railroad owned
                instructionToReturn = f"PayRailroad:{self.index}"

            elif (
                self.color == "Utility"
            ):  # Rent is based on dice roll, number times 4 if one utility owned, 10 if both
                instructionToReturn = f"PayUtility:{self.index}"

            else:  # Standard property
                instructionToReturn = f"Pay:{self.index}"

        return instructionToReturn

    # Return the rent value for the current property
    def getRent(self) -> int:
        return self.rent

    # Return the amount of money needed to buy the property
    def getCost(self) -> int:
        return self.cost

    # Owner is an index value representing one of the players
    def getOwner(self) -> int:
        return self.owner

    # Set owner of the current property
    def setOwner(
        self, newOwner: int
    ) -> None:  # A new player index is assigned to self.owner.
        self.owner = newOwner

    # Return the color of the current property
    def getColor(self) -> str:
        return self.color


# Starting tile
class Go(Tile):
    def __init__(
        self, index
    ) -> None:  # Landing on our passing go giving $200 is handle in the move function
        super().__init__(index)

    def landedOn(self) -> str:
        return "ToGo"


# Quite literally, does nothing.
class FreeParking(Tile):
    def __init__(self, index) -> None:
        super().__init__(index)

    def landedOn(self) -> str:  # Blank string means doing nothing
        return "ToFreeParking"  # 20 is the index of the jail


# Sends the player to jail
class GoToJail(Tile):
    def __init__(self, index: int) -> None:
        super().__init__(index)

    def landedOn(self) -> str:
        return "ToJail"


# Does nothing when landed on, jail logic handled by player class.
class Jail(Tile):
    def __init__(self, index: int) -> None:
        super().__init__(index)

    def landedOn(self) -> str:
        return ""


# Draw a chance card when landed on, parsing of card effects handled in the player class
class Chance(Tile):
    def __init__(self, index: int) -> None:
        super().__init__(index)

    def landedOn(self, flavorInfo) -> str:
        # Draw the card
        chaCard: card.ChanceCard = card.ChanceCard()
        effect: card.CardReturn = chaCard.getEffect()

        flavorInfo.text = effect.flavorText
        amount = effect.randomAmount
        flavorInfo.amount = amount

        # self.displayCard(screen, text, amount)

        # If the card effect is money based
        if isinstance(effect.requirement, cardTypes.MoneyFlavor):
            match effect.requirement.transfer:
                case "toOtherPlayers":
                    return f"PayAll:{amount}"
                case "fromOtherPlayers":
                    return f"ReceiveFromAll:{amount}"

        # If the card is movment based
        elif isinstance(effect.requirement, cardTypes.MovementFlavor):
            match effect.requirement.direction:
                case "toJail":
                    return f"ToJail"
                case "forwards":
                    return f"MoveAll:{amount}"
                case "backwards":
                    return f"MoveAll:{-amount}"

        # Get out of jail free card
        else:
            return "GetOutCard"


# Draw a community chest card when landed on, parsing of card effects handled in the player class
class CommunityChest(Tile):
    def __init__(self, index: int) -> None:
        super().__init__(index)

    def landedOn(self, flavorInfo) -> str:
        # Draw the card
        comCard: card.CommunityCard = card.CommunityCard()
        effect: card.CardReturn = comCard.getEffect()

        flavorInfo.text = effect.flavorText
        amount = effect.randomAmount
        flavorInfo.amount = amount

        # If the card effect is money based
        if isinstance(effect.requirement, cardTypes.MoneyFlavor):
            match effect.requirement.transfer:
                case "toBank":
                    return f"Charge:{amount}"
                case "fromBank":
                    return f"Charge:{-amount}"

        # If the card is movment based
        elif isinstance(effect.requirement, cardTypes.MovementFlavor):
            match effect.requirement.direction:
                case "toRailroad":
                    return "ToRailroad"
                case "backToGo":
                    return f"ToGo"
                case "freeParking":
                    return f"ToFreeParking"

        # Get out of jail free card
        else:
            return "GetOutCard"


# Pay $200 when landed on
class IncomeTax(Tile):
    def __init__(self, index: int) -> None:
        super().__init__(index)

    # Player pays $200
    def landedOn(self) -> str:
        return "Charge:200"


# Pay $100 when landed on
class LuxuryTax(Tile):
    def __init__(self, index: int) -> None:
        super().__init__(index)

    # Player pays $100
    def landedOn(self) -> str:
        return "Charge:100"
