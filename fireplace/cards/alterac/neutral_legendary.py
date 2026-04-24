from ..utils import *

##
# Minions


class AV_100:
    """Drek'Thar"""

    # [x]<b>Battlecry</b>: If this costs more than every minion in your deck,
    # summon 2 of them.
    powered_up = -Find(FRIENDLY_DECK + MINION + (COST <= COST(SELF)))
    play = powered_up & Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION, 2))


class AV_223:
    """Vanndar Stormpike"""

    # [x]<b>Battlecry</b>: If this costs less than every minion in your deck,
    # reduce their Cost by (3).
    powered_up = -Find(FRIENDLY_DECK + MINION + (COST >= COST(SELF)))
    play = powered_up & Buff(FRIENDLY_DECK + MINION, "AV_223e")


class AV_223e:
    tags = {GameTag.COST: -3}
    events = REMOVED_IN_PLAY
