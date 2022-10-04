class Bank():
    def __init__(self, numHouses, numHotels):
        self.numHouses = numHouses            # Number of houses available to players
        self.numHotels = numHotels            # Number of hotels available to players

    def drawChanceCard(self, player) -> None:
        pass

    def drawCommunityCard(self, player) -> None:
        pass

    def getHouseCount(self) -> int:
        return self.numHouses

    def getHotelCount(self) -> int:
        return self.numHotels
