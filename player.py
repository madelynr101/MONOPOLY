import tile  # One of these may or may not be the way of doing it
import random

class Player():
    def __init__(self):
        self.money = 0  # The amount of money the player currently has
        self.properties = [] #properties play owns
        self.location = 0  # Index value for the tile the player is currently
        self.getOutOfJailCards = 0  # The number of get out of jail free cards the player currently has
        self.isInJail = False  # Is the player currently in jail
        self.doubleRolls = 0 # Increases whenever the player rolls doubles, set back to zero when they don't 
        self.piece = 0  # Index of the players piece
        self.isBankrupt = False  # Is the player currently bankrupt

    #pay another player
    def pay(self, landedOn: tile.Property) -> None:
        cost = 0 #wherever we get cost, varies based on propery and houses / hotels
        if self.money >= cost:
            self.money -= cost
            landedOn.owner.getMoney(cost)
        else: #if we don't have enough just give them
            landedOn.owner.getMoney(self.money)
            self.isBankrupt = True

    #simply get money, or send money to bank
    def getMoney(self, amount: int) -> None:
        self.money += amount
        if (self.money < 0):
            self.isBankrupt = True
        pass

    # Simulate dice roll, two random numbers 1-6, mark if doubles, returns the rolled value
    def roll(self) -> int:
        diceOne = random.randint(1, 6)
        diceTwo = random.randint(1, 6)

        if diceOne == diceTwo:
            self.doubleRolls += 1

        else:
            self.doubleRolls = 0

        return diceOne + diceTwo

    #move a given distance
    def move(self, distance: int, board: tile.Tile[]):
        moved = 0
        while(moved < distance):
            self.index = index+1
            if self.index >= len(board):
                self.index = 0
            moved += 1
        board[index].landedOn(self)
        