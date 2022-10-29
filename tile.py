from abc import ABCMeta, abstractmethod
from card import *
from cardTypes import *


class Tile(metaclass=ABCMeta):
    def __init__(self, index) -> None:
        self.index = index

    @abstractmethod
    def landedOn(self) -> str:
        pass

    def getIndex(self) -> int:
        return self.index


class Property(Tile):
    def __init__(self, index):
        super().__init__(index)
        self.owner = None
        self.cost = 0
        self.rent = 0
        self.color = None
        # self.houses = 0  # Stretch goals
        # self.hotels = 0
        # self.mortgaged = False

    def __init__(self, index, cost, rent, color):
        super().__init__(index)
        self.owner = None
        self.cost = cost
        self.rent = rent
        self.color = color

    def landedOn(self, landingPlayer: int) -> str:
        instructionToReturn = ""

        if self.owner == None:  # If no one owns this property
            instructionToReturn = f"Purchase:{self.index}"  # Player will handle having enough money / if they want to but it

        elif (
            self.owner != landingPlayer
        ):  # If property is owned, but not by current player (landing player owning property does nothing)
            if self.color == "Railroad":  # Rent increases for each railroad owned
                instructionToReturn = f"PayRailroad:{self.index}"

            elif (
                self.color == "Utility"
            ):  # Rent is based on dice roll, number times 4 if one utility owned, 10 if both
                instructionToReturn = f"PayUtility:{self.index}"

            else:  # Standard property
                instructionToReturn = f"Pay:{self.index}"

        return instructionToReturn

    def getRent(self) -> int:  # Return the rent value for the current property
        return self.rent

    def getCost(self) -> int:  # Return the amount of money needed to buy the property
        return self.cost

    def getOwner(
        self,
    ) -> int:  # Owner is an index value representing one of the players
        return self.owner

    def setOwner(
        self, newOwner: int
    ) -> None:  # A new player index is assigned to self.owner.
        self.owner = newOwner

    def getColor(self) -> str:
        return self.color

    # def addHouse(self) -> None:
    #   pass


class Go(Tile):
    def __init__(
        self, index
    ) -> None:  # Landing on our passing go giving $200 is handle in the move function
        super().__init__(index)

    def landedOn(self) -> str:
        return "Move:0"


# Quite literally, does nothing.
class FreeParking(Tile):
    def __init__(self, index) -> None:
        super().__init__(index)

    def landedOn(self) -> str:  # Blank string means doing nothing
        return "Move:20"  # 20 is the index of the jail


class GoToJail(Tile):
    def __init__(self, index) -> None:
        super().__init__(index)

    def landedOn(self) -> str:
        return "ToJail"


# Does nothing when landed on, jail logic handled by player class.
class Jail(Tile):
    def __init__(self, index) -> None:
        super().__init__(index)

    def landedOn(self) -> str:
        return ""


class Chance(Tile):
    def __init__(self, index) -> None:
        super().__init__(index)

    def landedOn(self) -> str:
        chaCard: ChanceCard = ChanceCard()
        effect: CardReturn = chaCard.getEffect()

        if isinstance(effect.requirement, MoneyFlavor):
            match effect.requirement.transfer:
                case "toOtherPlayers":
                    return f"PayAll:{effect.randomAmount}"
                case "fromOtherPlayers":
                    return f"ReceiveFromAll:{effect.randomAmount}"
        elif isinstance(effect.requirement, MovementFlavor):
            match effect.requirement.direction:
                case "toJail":
                    return f"ToJail"
                case "forwards":
                    return f"MoveAll:{effect.randomAmount}"
                case "backwards":
                    return f"MoveAll:{-effect.randomAmount}"
        else:
            return "GetOutCard"


class CommunityChest(Tile):
    def __init__(self, index) -> None:
        super().__init__(index)

    def landedOn(self) -> str:
        comCard: CommunityCard = CommunityCard()
        effect: CardReturn = comCard.getEffect()

        if isinstance(effect.requirement, MoneyFlavor):
            match effect.requirement.transfer:
                case "toBank":
                    return f"Charge:{effect.randomAmount}"
                case "fromBank":
                    return f"Charge:{-effect.randomAmount}"
        elif isinstance(effect.requirement, MovementFlavor):
            match effect.requirement.direction:
                case "toRailroad":
                    return "ToRailroad"
                case "backToGo":
                    return f"Move:0"
                case "freeParking":
                    return f"Move:20"
        else:
            return "GetOutCard"


class IncomeTax(Tile):
    def __init__(self, index) -> None:
        super().__init__(index)

    def landedOn(self) -> str:
        # Player pays $200 to bank
        return "Charge:200"  # I do believe this pays $200 to the bank, the pay function is specifically for properties


class LuxuryTax(Tile):
    def __init__(self, index) -> None:
        super().__init__(index)

    def landedOn(self) -> str:
        # Will require the player to pay $100 to the bank if landed on.
        return "Charge:100"  # Pay $100 to bank


def tileTest() -> None:
    for _ in range(10):
        chanceTile: Chance = Chance(0)
        communityTile: CommunityChest = CommunityChest(1)

        print(f"{chanceTile.landedOn()=}, {communityTile.landedOn()=}")


if __name__ == "__main__":
    tileTest()
