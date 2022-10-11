from enum import Enum
from dataclasses import dataclass
from typing import Union


class MoveEnum(Enum):
    JAIL: int = 7
    BACK_TO_GO: int = 8
    FREE_PARKING: int = 9
    NEAREST_RAILROAD: int = 10


class ConsumableCards(Enum):
    GET_OUT_OF_JAIL_FREE_CARD: int = 11


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


@dataclass
class CardReturn:
    flavorText: str
    type: str
    requirement: Union[MovementFlavor, MoneyFlavor, None]
    randomAmount: Union[int, MoveEnum, ConsumableCards]
