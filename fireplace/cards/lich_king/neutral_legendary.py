from ..utils import *

##
# Spells


class RLK_590:
    """The Sunwell"""

    # Fill your hand with random spells. Costs (1) less for each other card in
    # your hand.
    cost_mod = -Count(FRIENDLY_HAND - SELF)
    play = Give(CONTROLLER, RandomSpell()) * (
        MAX_HAND_SIZE(CONTROLLER) - Count(FRIENDLY_HAND)
    )
