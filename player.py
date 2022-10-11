import tile
import random
from typing import List
from datetime import datetime

random.seed(datetime.now())

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

    def getProperties(self) -> str:
        propList = ""
        for prop in self.properties:
            propList += f"{prop.getIndex()}, "

        return propList

    # pay another player
    def pay(self, landedOn: tile.Property, playerList) -> None:
        cost = landedOn.getRent() #wherever we get cost, varies based on propery and houses / hotels
        if self.money >= cost:
            self.money -= cost
            playerList[landedOn.getOwner()].money += cost
        else: #if we don't have enough just give them all we have
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
        
        if isinstance(board[self.location], tile.Property):
            effect = board[self.location].landedOn(self.piece)
        else:
            effect = board[self.location].landedOn()
            
        self.landOnParse(effect, board, playerList)
        #TODO: Remove test print
        print(f"player {self.piece} has reached space {self.location}")
        
    def landOnParse(self, effect: str, board: tile.Tile, playerList) -> None:
        instructions = effect.split(':')
        print(f'{effect=}')
        if len(instructions) > 1:
            amount: int = int(instructions[1])
        
        match instructions[0]:
            case 'Charge':
                self.bankTransaction(-amount)

            case 'ReceiveFromAll':  # All other players give you money
                pass

            case 'Pay':  # board[amount] should be the inedex value of the property being landed on
                self.pay(board[amount], playerList)

            case 'PayRailroad':
                totalCost = board[amount].getRent()
                railroadAmt = 0
                for prop in playerList[board[amount].getOwner()].properties:
                    if prop.getColor() == 'Railroad':
                        railroadAmt += 1
                
                for i in range(1, railroadAmt):
                    totalCost *= 2

                if(totalCost >= self.money):
                    playerList[board[amount].getOwner()].money += self.money
                    self.money = 0
                    self.isBankrupt = True

                else:
                    playerList[board[amount].getOwner()].money += totalCost
                    self.money -= totalCost

            case 'PayUtility':  # Utility indexes are 12 and 28
                amountDue = random.randint(1, 6)  # Roll a dice
                
                if (board[12].getOwner() == board[28].getOwner()):  # If the same player ownes both utilities
                    amountDue *= 10
                    
                else:  # Player only owens one utility
                    amountDue *= 4

                self.money -= amountDue
                # TODO Give the other player that money
                

            case 'PayAll':  # You give all other players money
                pass

            case 'Purchase':  # Note that 'amount' here reffers to the inedex of the tile being purchased
                if board[amount].getCost() < self.money:  # Force buy property if you can afford it 
                    self.money -= board[amount].getCost()  # TODO Make purchasing optional
                    self.properties.append(board[amount])
                    board[amount].setOwner(self.piece)
            
            case 'Move':
                if amount < 0:
                    for i in range(-amount):
                        self.location -= 1
                        if self.location < 0:
                            self.location = len(board) - 1
                else:
                    for i in range(amount):
                        self.location += 1
                        if self.location >= len(board):
                            self.location = 0
                            self.bankTransaction(200)
            
            case 'ToJail':
                self.isInJail = True
				
            case 'GetOutCard':
                self.getOutOfJailCards += 1

            case 'toRailroad':
                railroadLocs = [5, 15, 25, 35]
                currClosestLoc = len(board)
                for loc in railroadLocs:
                    if self.location - railroadLocs <= currClosestLoc:
                        currClosestLoc = loc
                
                self.location = currClosestLoc

            case 'MoveAll':
                for player in playerList:
                    # Copied from the 'Move' case above
                    if int(amount) < 0:
                        for i in range(-amount):
                            player.location -= 1
                            if player.location < 0:
                                player.location = len(board) - 1
                    else:
                        for i in range(amount):
                            player.location += 1
                            if player.location >= len(board):
                                player.location = 0
                                player.bankTransaction(200)


    def escapeJail(self, dice: List[int]) -> None:
        if dice[0] == dice[1]:
            self.isInJail = False
        
