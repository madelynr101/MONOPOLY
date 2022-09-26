import card
import player

class Bank():
    def __init__(self, numHouses, numHotels, chanceCards, communityCards):
        self.numHouses = numHouses            # Number of houses available to players
        self.numHotels = numHotels            # Number of hotels available to players
        self.chanceCards = chanceCards        # List of chance cards in play
        self.communityCards = communityCards  # List of community chest cards in play

    def drawChanceCard(self, p: Player) -> None:
        pass

    def drawCommunityCard(self, p: Player) -> None:
        pass

    def getHouseCount() -> int:
        return self.houses

    def getHotelCount() -> int:
        return self.hotels
