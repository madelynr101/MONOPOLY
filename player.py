import tile
import random
from typing import List
from datetime import datetime

random.seed(datetime.now())

jailIndex = 10

class Player():
    def __init__(self, pieceIn, AI):
        self.money = 1500  # The amount of money the player currently has
        self.properties = [] #properties play owns
        self.location = 0  # Index value for the tile the player is currently
        self.getOutOfJailCards = 0  # The number of get out of jail free cards the player currently has
        self.isInJail = False  # Is the player currently in jail
        self.doubleRolls = 0 # Increases whenever the player rolls doubles, set back to zero when they don't 
        self.piece = pieceIn  # Index of the players piece
        self.isBankrupt = False  # Is the player currently bankrupt
        self.isAI = AI

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
        else: #if we don't have enough just give them all we have and are noe bankrupt
            playerList[landedOn.getOwner()].money += self.money
            self.money -= cost
            self.isBankrupt = True
            self.RemoveProperties()

    # Get or pay money to the bank, amount can be positive or negative, with
    # negative meaning loss of money and positive meaning gain.
    def bankTransaction(self, amount: int) -> None:
        if(self.money + amount > 0):
            self.money += amount
        else:  # If we don't have enough money to pay, we lost all we have and are bankrupt
            self.money = 0
            self.isBankrupt = True
            self.RemoveProperties()

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
       
        if self.doubleRolls == 3:
            self.toJail()
        
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
            instructionValue: int = int(instructions[1])  # This value will either be a dollar amount or a tile index depending on the contex
        
        match instructions[0]:
            case 'Charge':
                self.bankTransaction(-instructionValue)  # instructionValue is a dollar amount

            case 'ReceiveFromAll':  # All other players give you money
                # TODO Impliment
                # instructionValue is a dollar amount owed in this context 
                for player in playerList:
                    if player.piece != self.piece:
                        if (player.money < instructionValue):  # Player can't afford, they go bankrupt
                            self.money += player.money  # Give money the player has
                            player.money = 0
                            player.isBankrupt = True
                            self.RemoveProperties()
                        else:  # Players can afford to pay
                            # TODO finish this
                            pass
                pass

            case 'Pay':  # board[instructionValue] should be the inedex value of the property being landed on
                self.pay(board[instructionValue], playerList)

            case 'PayRailroad':
                totalCost = board[instructionValue].getRent()  # instructionValue is a tile index here
                railroadAmt = 0
                for prop in playerList[board[instructionValue].getOwner()].properties:
                    if prop.getColor() == 'Railroad':
                        railroadAmt += 1
                
                for i in range(1, railroadAmt):
                    totalCost *= 2

                if(totalCost >= self.money):  # Can't affor rent, bankrupt
                    playerList[board[instructionValue].getOwner()].money += self.money
                    self.money = 0
                    self.isBankrupt = True
                    self.RemoveProperties()

                else:
                    playerList[board[instructionValue].getOwner()].money += totalCost
                    self.money -= totalCost

            case 'PayUtility':  # Utility indexes are 12 and 28
                amountDue = random.randint(1, 6)  # Roll a dice
                
                if (board[12].getOwner() == board[28].getOwner()):  # If the same player ownes both utilities
                    amountDue *= 10
                    
                else:  # Player only owns one utility
                    amountDue *= 4

                if (amountDue >= self.money):  # Can't afford rent, bankrupt
                    playerList[board[instructionValue].getOwner()].money += self.money  # Give player all we have left
                    self.money = 0
                    self.isBankrupt = True
                    self.RemoveProperties()  # All owned properties return to the bank
                
                else:  # Pay rent calculated above
                    playerList[board[instructionValue].getOwner()].money += amountDue
                    self.money -= amountDue
                

            case 'PayAll':  # You give all other players money
                for player in playerList:
                   if player.piece != self.piece:
                        if self.money >= instructionValue:
                            player.money += instructionValue
                            self.money -= instructionValue
                        else:
                            player.money += self.money
                            self.money = 0
                            
                        if self.money == 0:
                            self.isBankrupt = True
                            break

            case 'Purchase':  # Note that 'amount' here reffers to the inedex of the tile being purchased
                if not self.isAI:
                    #TODO: dialog box that returns some kind of boolean. Return if not looking to buy, else continue
                    pass
                
                if board[instructionValue].getCost() < self.money:  # Force buy property if you can afford it 
                    self.money -= board[instructionValue].getCost()  # TODO Make purchasing optional
                    self.properties.append(board[instructionValue])
                    board[instructionValue].setOwner(self.piece)
                else:
                    print("Can't afford property!")
            
            case 'Move':
                if instructionValue < 0:
                    for i in range(-instructionValue):
                        self.location -= 1
                        if self.location < 0:
                            self.location = len(board) - 1
                else:
                    for i in range(instructionValue):
                        self.location += 1
                        if self.location >= len(board):
                            self.location = 0
                            self.bankTransaction(200)
            
            case 'ToJail':
                self.toJail()
				
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
                    if instructionValue < 0:
                        for i in range(-instructionValue):
                            player.location -= 1
                            if player.location < 0:
                                player.location = len(board) - 1
                    else:
                        for i in range(instructionValue):
                            player.location += 1
                            if player.location >= len(board):
                                player.location = 0
                                player.bankTransaction(200)


    def escapeJail(self, dice: List[int]) -> None:
        if dice[0] == dice[1]:
            self.isInJail = False
        

    def RemoveProperties(self) -> None:  # Called when a player goes bankrupt, returns all of thier properties to the bank
        for OwnedItem in self.properties:
            OwnedItem.Owner = None  
        self.properties = []

    def toJail(self) -> None:
        self.index = jailIndex
        self.isInJail = True