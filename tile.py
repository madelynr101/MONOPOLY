from abc import abstractmethod
from card import *
from cardTypes import *

class Tile():
  def __init__(self, index) -> None:
    self.index = index

  @abstractmethod
  def landedOn(self) -> str:
    pass

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

  def getOwner(self) -> int:
    return self.owner

  def landedOn(self, landingPlayer: int) -> str:
    instructionToReturn = ""
    if self.owner == None:  # If no one owns this property
      instructionToReturn = f"Purchase:{self.index}"  # Player will handle having enough money / if they want to but it
    elif self.owner != landingPlayer:  # Currently player doesn't own the property
      instructionToReturn = f"Charge:{self.rent}"

    return instructionToReturn

  # TODO Special cases for railroads
  # TODO Special cases for utilies

  def getRent(self) -> int:  # Return the rent value for the current property
    return self.rent

  def getOwner(self) -> int:  # Owner is an index value representing one of the players
    return self.owner

  def setOwner(self, newOwner: int) -> None: # A new player index is assigned to self.owner.
    self.owner = newOwner

  def purchase(self, landingPlayer: int) -> None:
    landingPlayer.bankTransaction(-self.cost)

  # def addHouse(self) -> None:
  #   pass


class Go(Tile):
  def __init__(self, index) -> None:  # Landing on our passing go giving $200 is handle in the move function
    super().__init__(index)
  
  def landedOn(self, landingPlayer: int) -> str:
    return ''
    

# Quite literally, does nothing.
class FreeParking(Tile):
  def __init__(self, index) -> None:
    super().__init__(index)

  def landedOn(self, landingPlayer: int) -> str:  # Blank string means doing nothing
    return ''

class GoToJail(Tile):
  def __init__(self, index) -> None:
    super().__init__(index)

  def landedOn(self, landingPlayer: int) -> str:
    return "To:Jail"
  
# Does nothing when landed on, jail logic handled by player class.
class Jail(Tile):
  def __init__(self, index) -> None:
    super().__init__(index)

  def landedOn(self, landingPlayer: int) -> str:
    return ''

class Chance(Tile):
  def __init__(self, index) -> None:
    super().__init__(index)

  def landedOn(self, landingPlayer: int) -> str:
    chaCard: ChanceCard = ChanceCard()
    effect: CardReturn = chaCard.getEffect()

    # TODO change this to use the card's effect
    return "Draw:Chance"

class CommunityChest(Tile):
  def __init__(self, index) -> None:
    super().__init__(index)

  def landedOn(self, landingPlayer: int) -> str:
    comCard: CommunityCard = CommunityCard()
    effect: CardReturn = comCard.getEffect()

    # TODO change this to use the card's effect
    return "Draw:Chest"

class IncomeTax(Tile):
  def __init__(self, index) -> None:
    super().__init__(index)

  def landedOn(self, landingPlayer: int) -> str:
    # Player pays $200 to bank
    return "Charge:200" # I do believe this pays $200 to the bank, the pay function is specifically for properties

class LuxuryTax(Tile):
  def __init__(self, index) -> None:
    super().__init__(index)

  def landedOn(self, landingPlayer: int) -> str:
    # Will require the player to pay $100 to the bank if landed on.
    return "Charge:100" # Pay $100 to bank