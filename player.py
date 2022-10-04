import tile
import random
from typing import List

class Player():
    def __init__(self, pieceIn):
        self.money = 0  # The amount of money the player currently has
        self.properties = [] #properties play owns
        self.location = 0  # Index value for the tile the player is currently
        self.getOutOfJailCards = 0  # The number of get out of jail free cards the player currently has
        self.isInJail = False  # Is the player currently in jail
        self.doubleRolls = 0 # Increases whenever the player rolls doubles, set back to zero when they don't 
        self.piece = pieceIn  # Index of the players piece
        self.isBankrupt = False  # Is the player currently bankrupt

    # pay another player
    def pay(self, landedOn: tile.Property) -> None:
        cost = landedOn.getRent() #wherever we get cost, varies based on propery and houses / hotels
        if self.money >= cost:
            self.money -= cost
            landedOn.owner.getMoney(cost)
        else: #if we don't have enough just give them
            landedOn.owner.getMoney(self.money)
            self.isBankrupt = True

    # Get or pay money to the bank
    def bankTransaction(self, amount: int) -> None:
        self.money += amount
        if (self.money < 0):
            self.isBankrupt = True
        pass

    # Simulate dice roll, two random numbers 1-6, mark if doubles, returns the rolled value
    def roll(self) -> List[int]:
        diceOne = random.randint(1, 6)
        diceTwo = random.randint(1, 6)

        if diceOne == diceTwo:
            self.doubleRolls += 1

        else:
            self.doubleRolls = 0

        return [diceOne,diceTwo]

    #move a given distance
    def move(self, board: List[tile.Tile]):
        dice = self.roll(self)
        if self.isInJail:  
            # TODO Once we have pygame figured out, we need an option to pay $50 to leave jail early
            # TODO If a player has a get out of jail free card, they can use it to get out of jail 
            self.escapeJail(self,dice)
            return
       
        distance = dice[0] + dice[1]
        moved = 0
        while(moved < distance):
            self.index = self.index+1
            if self.index >= len(board):
                self.index = 0
                self.bankTransaction(self, 200)
            moved += 1
        effect = board[self.index].landedOn
        self.landOnParse(effect)
        #TODO: Remove test print
        print("player " + self.piece + " has reached space " + self.index)
        
    def landOnParse(self, effect: str) -> None:
        instructions = effect.split(':')
        match instructions[0]:
            case 'Charge':
                self.bankTransaction(-int(instructions[1]))
            case 'To':
                self.location = int(instructions[1])
            case 'Draw':
                
            case 'Pay':
                self.pay(board[])
            case 'Purchase':
                pass


    def escapeJail(self, dice: List[int]) -> None:
        if dice[0] == dice[1]:
            self.isInJail = False
        
