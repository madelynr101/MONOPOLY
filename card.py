from io import FileIO
from json import load
from abc import abstractmethod
from typing import Union
from random import randint, random
from cardTypes import *

class Card():
    def __init__(self) -> None:
        self.chanceFlavor: list[Flavor] = []
        self.communityFlavor: list[Flavor] = []

        self.readFlavorFromFile()

    def setChanceEffects(self, chance) -> None:
        chanceEffect = chance["effect"]

        if chanceEffect["type"] == "money":
            combined: CombinedFlavor = CombinedFlavor(type=chanceEffect["type"], semantics=MoneyFlavor(transfer=chanceEffect["transfer"]), affects=chanceEffect["affects"])
            self.chanceFlavor.append(Flavor(text=chance["text"], effect=combined))
        elif chanceEffect["type"] == "movement":
            combined: CombinedFlavor = CombinedFlavor(type=chanceEffect["type"], semantics=MovementFlavor(direction=chanceEffect["direction"]), affects=chanceEffect["affects"])
            self.chanceFlavor.append(Flavor(text=chance["text"], effect=combined))
        elif chanceEffect["type"] == "consumable":
            combined: CombinedFlavor = CombinedFlavor(type=chanceEffect["type"], semantics=None, affects=chanceEffect["affects"])
            self.chanceFlavor.append(Flavor(text=chance["text"], effect=combined))

    def setCommunityEffects(self, community) -> None:
        communityEffect = community["effect"]
        
        if communityEffect["type"] == "money":
            combined: CombinedFlavor = CombinedFlavor(type=communityEffect["type"], semantics=MoneyFlavor(transfer=communityEffect["transfer"]), affects=communityEffect["affects"])
            self.communityFlavor.append(Flavor(text=community["text"], effect=combined))
        elif communityEffect["type"] == "movement":
            combined: CombinedFlavor = CombinedFlavor(type=communityEffect["type"], semantics=MovementFlavor(direction=communityEffect["direction"]), affects=communityEffect["affects"])
            self.communityFlavor.append(Flavor(text=community["text"], effect=combined))
        elif communityEffect["type"] == "consumable":
            combined: CombinedFlavor = CombinedFlavor(type=communityEffect["type"], semantics=None, affects=communityEffect["affects"])
            self.communityFlavor.append(Flavor(text=community["text"], effect=combined))

    def readFlavorFromFile(self) -> None:
        file: FileIO = open("cardFlavor.json")

        data = load(file)

        chance = data["Chance"]
        community = data["Community"]


        for i in range(len(chance)):
            self.setChanceEffects(chance[i])
            self.setCommunityEffects(community[i])

    @abstractmethod
    def getEffect(self) -> str:
        pass

    @abstractmethod
    def getRandomFlavorText(self) -> str:
        pass

    @abstractmethod
    def getRandomAmount(self) -> Union[int, MoveEnum]:
        pass


class ChanceCard(Card):
    def __init__(self) -> None:
        super().__init__()

    def getEffect(self) -> str:
        randomVal: int = randint(0, len(self.chanceFlavor) - 1)

        card: Flavor = self.chanceFlavor[randomVal]

        flavorText: str = self.getRandomFlavorText(card)

        randomAmount: Union[int, MoveEnum, ConsumableCards] = 0

        if card.effect.type == "money":
            randomAmount = self.getRandomAmount(card.effect.semantics.transfer)
        elif card.effect.type == "movement":
            randomAmount = self.getRandomAmount(card.effect.semantics.direction)
        else:
            # Can be modified to call getRandomAmount if we desire more consumable cards
            randomAmount = ConsumableCards.GET_OUT_OF_JAIL_FREE_CARD
        
        # Remove for production build
        print(f"{flavorText=}, {card.effect.type=}, {randomAmount=}")

    def getRandomFlavorText(self, card: Flavor) -> str:
        return card.text
    
    def getRandomAmount(self, type: str) -> Union[int, MoveEnum]:
        match type:
            # Money cases
            case "toOtherPlayers":
                return randint(1, 3) * 50
            case "fromOtherPlayers":
                return randint(1, 3) * 100
            # Movement cases
            case "forwards":
                return randint(1, 6)
            case "backwards":
                return randint(1, 6)
            case "toJail":
                return MoveEnum.JAIL

class CommunityCard(Card):
    def __init__(self) -> None:
        super().__init__()

    def getEffect(self) -> str:
        randomVal: int = randint(0, len(self.communityFlavor) - 1)

        card: Flavor = self.communityFlavor[randomVal]

        flavorText: str = self.getRandomFlavorText(card)

        randomAmount: Union[int, MoveEnum, ConsumableCards] = 0

        if card.effect.type == "money":
            randomAmount = self.getRandomAmount(card.effect.semantics.transfer)
        elif card.effect.type == "movement":
            randomAmount = self.getRandomAmount(card.effect.semantics.direction)
        else:
            # Can be modified to call getRandomAmount if we desire more consumable cards
            randomAmount = ConsumableCards.GET_OUT_OF_JAIL_FREE_CARD

        # Remove for production build
        print(f"{flavorText=}, {card.effect.type=}, {randomAmount=}")
    
    def getRandomFlavorText(self, card: Flavor) -> str:
        return card.text
    
    def getRandomAmount(self, type: str) -> Union[int, MoveEnum]:
        match type:
            # Money cases
            case "toBank":
                return randint(1, 3) * 100
            case "fromBank":
                return randint(2, 5) * 100
            # Movement cases
            case "freeParking":
                return MoveEnum.FREE_PARKING
            case "backToGo":
                return MoveEnum.BACK_TO_GO
            case "toRailroad":
                return MoveEnum.NEAREST_RAILROAD

def main() -> None:
    for _ in range(10):
        chanceCard: ChanceCard = ChanceCard()
        communityCard: CommunityCard = CommunityCard()

        chanceCard.getEffect()
        communityCard.getEffect()

if __name__ == "__main__": # Driver for testing
    main()