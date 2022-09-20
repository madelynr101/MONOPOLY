from io import FileIO
from json import load
from abc import abstractmethod
from typing import Union
from dataclasses import dataclass

@dataclass
class MoneyFlavor:
    transfer: str

@dataclass
class MovementFlavor:
    direction: str

@dataclass
class CombinedFlavor:
    type: str
    semantics: Union[MovementFlavor, MoneyFlavor, None]
    affects: str

@dataclass
class Flavor:
    text: str
    effect: CombinedFlavor

class Card():
    def __init__(self) -> None:
        self.chanceFlavor: list[Flavor] = []
        self.communityFlavor: list[Flavor] = []

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

        for _ in range(len(chance)):
            self.setChanceEffects(chance)
            self.setCommunityEffects(community)

    @abstractmethod
    def getEffect(self) -> str:
        pass

    @abstractmethod
    def getRandomFlavorText(self) -> str:
        pass

    @abstractmethod
    def getRandomAmount(self) -> Union[float, int]:
        pass


class ChanceCard(Card):
    def __init__(self) -> None:
        super().__init__()

    def getEffect(self) -> str:
        pass
    
    def getRandomFlavorText(self) -> str:
        pass
    
    def getRandomAmount(self) -> Union[float, int]:
        pass

class CommunityCard(Card):
    def __init__(self) -> None:
        super().__init__()

    def getEffect(self) -> str:
        pass
    
    def getRandomFlavorText(self) -> str:
        pass
    
    def getRandomAmount(self) -> Union[float, int]:
        pass