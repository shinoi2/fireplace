from ..utils import *

##
# Minions


class CS3_005:
    """Vanessa VanCleef"""

    # <b>Combo:</b> Add a copy of the last card your opponent played to your
    # hand.
    combo = Give(CONTROLLER, Copy(ENEMY_CARDS_PLAYED_THIS_GAME[-1:]))
