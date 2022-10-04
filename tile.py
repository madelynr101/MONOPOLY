from abc import abstractmethod
import player
import card

'''
obj = Property(1, 50, 20, "Brown")  # Something like this may or may not be correct

'''

class Tile():
  def __init__(self, index) -> None:
    self.index = index

  @abstractmethod
  def landedOn(self) -> None:
    pass

class Property(Tile):
  def __init__(self, index):
    super.__init__(self, index)
    self.owner = None
    self.cost = 0
    self.rent = 0
    self.color = None
    # self.houses = 0  # Stretch goals
    # self.hotels = 0
    # self.mortgaged = False

  def __init__(self, index, cost, rent, color):
    super.__init__(self, index)
    self.owner = None
    self.cost = cost
    self.rent = rent
    self.color = color

  def landedOn(self, landingPlayer: player) -> None:
    if self.owner == None:  # If no one owns this property
      if landingPlayer.money >= self.cost:  # TODO Let players chose if the want to purchase property
        self.purchase(self, landingPlayer)
    elif self.owner.piece != landingPlayer.piece:  # Currently player doesn't own the property
      landingPlayer.pay(self.rent)  # This (in theory) should take the rent from the current player and give it to player whose property it is

  # TODO Special cases for railroads
  # TODO Special cases for utilies

  def getRent(self) -> int:
    return self.rent

  def purchase(self, landingPlayer: player) -> None:
    landingPlayer.bankTransaction(-self.cost)

  # def addHouse(self) -> None:
  #   pass


class Go(Tile):
  def __init__(self, index) -> None:
    super.__init__(self, index)

  def landedOn(self, landingPlayer: player) -> None:
    landingPlayer.bankTransaction(200)  # Player recieves $200
    # Passing go is handled in the player class

# Quite literally, does nothing.
class FreeParking(Tile):
  def __init__(self, index) -> None:
    super.__init__(self, index)

class GoToJail(Tile):
  def __init__(self, index) -> None:
    super.__init__(self, index)

  def landedOn(self, landingPlayer: player) -> None:
    # Sets player location to jail and marks them as in jail
    landingPlayer.location = self.index - 1
    landingPlayer.isInJail = True
  
# Does nothing when landed on, jail logic handled by player class.
class Jail(Tile):
  def __init__(self, index) -> None:
    super.__init__(self, index)

class Chance(Tile):
  def __init__(self, index) -> None:
    super.__init__(self, index)

  def landedOn(self, landingPlayer: player) -> None:
    selectedCard = card.ChanceCard()  # This will draw a radom card
    selectedCard.getEffect()

class CommunityChest(Tile):
  def __init__(self, index) -> None:
    super.__init__(self, index)

  def landedOn(self, landingPlayer: player) -> None:
    selectedCard = card.CommunityCard()  # This will draw a radom card
    selectedCard.getEffect()

class IncomeTax(Tile):
  def __init__(self, index) -> None:
    super.__init__(self, index)

  def landedOn(self, landingPlayer: player) -> None:
    # Player pays $200 to bank
    landingPlayer.bankTransaction(-200)  # I do believe this pays $200 to the bank, the pay function is specifically for properties

class LuxuryTax(Tile):
  def __init__(self, index) -> None:
    super.__init__(self, index)

  def landedOn(self, landingPlayer: player) -> None:
    # Will require the player to pay $100 to the bank if landed on.
    landingPlayer.bankTransaction(-100)  # Pay $100 to bank