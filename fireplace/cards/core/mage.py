from ..utils import *

##
# Minions


class CS3_001:
    """Aegwynn, the Guardian"""

    # <b>Spell Damage +2</b> <b>Deathrattle:</b> The next minion_you draw
    # inherits these powers.
    deathrattle = Buff(CONTROLLER, "CS3_001e2")


class CS3_001e:
    tags = {
        SPELLPOWER: +2,
        DEATHRATTLE: True,
    }
    deathrattle = Buff(CONTROLLER, "CS3_001e2")


class CS3_001e2:
    events = Draw(CONTROLLER, MINION).on(Buff(Draw.TARGET, "CS3_001e"), Destroy(SELF))
