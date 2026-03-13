from ..utils import *

##
# Minions


class CS3_012:
    """Nordrassil Druid"""

    # <b>Battlecry:</b> The next spell you cast this turn costs_(3)_less.
    play = Buff(CONTROLLER, "CS3_012e")


class CS3_012e:
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -3})
    events = Play(CONTROLLER, SPELL).after(Destroy(SELF))
