from ..utils import *

##
# Minions


class CS3_015:
    """Selective Breeder"""

    # <b>Battlecry:</b> <b>Discover</b> a copy of a Beast in your deck.
    play = GenericChoice(
        CONTROLLER, Copy(RANDOM(DeDuplicate(FRIENDLY_DECK + BEAST)) * 3)
    )
