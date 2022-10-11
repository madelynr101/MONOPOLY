import tile
import random
from typing import List

class Player():
    def __init__(self, pieceIn):
        self.money = 1500  # The amount of money the player currently has
        self.properties = [] #properties play owns
        self.location = 0  # Index value for the tile the player is currently
        self.getOutOfJailCards = 0  # The number of get out of jail free cards the player currently has
        self.isInJail = False  # Is the player currently in jail
        self.doubleRolls = 0 # Increases whenever the player rolls doubles, set back to zero when they don't 
        self.piece = pieceIn  # Index of the players piece
        self.isBankrupt = False  # Is the player currently bankrupt

    # pay another player
    def pay(self, landedOn: tile.Property, playerList) -> None:
        cost = landedOn.getRent() #wherever we get cost, varies based on propery and houses / hotels
        if self.money >= cost:
            self.money -= cost
            playerList[landedOn.getOwner()].money += cost
        else: #if we don't have enough just give them
            playerList[landedOn.getOwner()].money += self.money
            self.money -= cost
            self.isBankrupt = True

    # Get or pay money to the bank, amount can be positive or negative, with
    # negative meaning loss of money and positive meaning gain.
    def bankTransaction(self, amount: int) -> None:
        if(self.money + amount > 0):
            self.money += amount
        else:
            self.money = 0
            self.isBankrupt = True

    # Simulate dice roll, two random numbers 1-6, mark if doubles, returns the rolled value
    def roll(self) -> List[int]:
        diceOne = random.randint(1, 6)
        diceTwo = random.randint(1, 6)

        if diceOne == diceTwo:
            self.doubleRolls += 1

        else:
            self.doubleRolls = 0

        return [diceOne, diceTwo]

    #move a given distance
    def move(self, board: List[tile.Tile], playerList):
        dice = self.roll()
        if self.isInJail:  
            # TODO Once we have pygame figured out, we need an option to pay $50 to leave jail early
            # TODO If a player has a get out of jail free card, they can use it to get out of jail 
            self.escapeJail(self,dice)
            return
       
        distance = dice[0] + dice[1]
        moved = 0
        while(moved < distance):
            self.location = self.location + 1
            if self.location >= len(board):
                print(f"Player {self.piece} passed Go!")
                self.location = 0
                self.bankTransaction(200)
            moved += 1
            
        effect = board[self.location].landedOn(self.piece)
        self.landOnParse(effect, board, playerList)
        #TODO: Remove test print
        print(f"player {self.piece} has reached space {self.location}")
        
    def landOnParse(self, effect: str, board: tile.Tile, playerList) -> None:
        instructions = effect.split(':')
        match instructions[0]:
            case 'Charge':
                self.bankTransaction(-int(instructions[1]))
            case 'Move':
                if instructions[1] < 0:
                    for i in range(-instructions[1]):
                        self.location -= 1
                        if self.location < 0:
                            self.location = len(board) - 1
                else:
                    for i in range(instructions[1]):
                        self.location += 1
                        if self.location >= len(board):
                            self.location = 0
                            self.bankTransaction(200)
						
            case 'Draw':
                pass
            case 'Pay':
                self.pay(board[instructions[1]], playerList)
            case 'Purchase':
                pass
            case 'ToJail':
                self.isInJail = True
				
            case 'GetOutCard':
                self.getOutOfJailCards += 1


    def escapeJail(self, dice: List[int]) -> None:
        if dice[0] == dice[1]:
            self.isInJail = False
        
