from abc import abstractmethod
from player import *

class Tile():
  def __init__(self, nextIndex) -> None:
    self.nextTile = nextIndex

  @abstractmethod
  def landedOn(self) -> None:
    pass

class Property(Tile):
  def __init__(self, nextIndex):
    super.__init__(self, nextIndex)
    self.owner = None
    self.cost = 0
    self.rent = 0
    self.color = None
    # self.houses = 0
    # self.hotels = 0
    # self.mortgaged = False

  def landedOn(self) -> None:
    pass

  def getRent(self) -> int:
    return self.rent

  def purchase(self) -> None:
    pass

  # def addHouse(self) -> None:
  #   pass


class Go(Tile):
  def __init__(self, nextIndex) -> None:
    super.__init__(self, nextIndex)

  def landedOn(self) -> None:
    # Player reiceves $200
    pass

class FreeParking(Tile):
  def __init__(self, nextIndex) -> None:
    super.__init__(self, nextIndex)

  def landedOn(self) -> None:
    # Quite literally, does nothing.
    pass

class IncomeTax(Tile):
  def __init__(self, nextIndex) -> None:
    super.__init__(self, nextIndex)

  def landedOn(self) -> None:
    # Player pays $200 to bank
    pass

class LuxuryTax(Tile):
  def __init__(self, nextIndex) -> None:
    super.__init__(self, nextIndex)

  def landedOn(self) -> None:
    # Will require the player to pay $100 to the bank if landed on.
    pass