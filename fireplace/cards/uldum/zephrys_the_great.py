from ..utils import *


class ULD_003:
    """Zephrys the Great"""

    # <b>Battlecry:</b> If your deck has no duplicates, wish for the perfect card.
    powered_up = -FindDuplicates(FRIENDLY_DECK)
    play = powered_up & GenericChoice(CONTROLLER, ZEPHRYS_POOL)
