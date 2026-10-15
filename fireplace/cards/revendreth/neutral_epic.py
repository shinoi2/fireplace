from ..utils import *

##
# Minions


class REV_960:
    """Ashen Elemental"""

    # [x]<b>Battlecry:</b> Whenever your opponent draws a card next turn, they
    # take 2 damage.
    play = Buff(OPPONENT, "REV_960e")


class REV_960e:
    events = (
        Draw(CONTROLLER).on(Find(CURRENT_PLAYER + CONTROLLER) & Hit(FRIENDLY_HERO, 2)),
        OWN_TURN_END.on(Destroy(SELF)),
    )


class REV_370:
    """Party Crasher"""

    # [x]<b>Battlecry:</b> Choose an enemy minion. Throw a random minion from
    # your hand at it.
    pass


class REV_017:
    """Insatiable Devourer"""

    # [x]<b>Battlecry:</b> Devour an enemy minion and gain its stats.
    # _<b>Infuse (@):</b> And its neighbors.
    pass


class MAW_032:
    """Tight-Lipped Witness"""

    # <b>Secrets</b> can't be revealed.
    pass


class REV_843:
    """Sinfueled Golem"""

    # <b>Infuse (@):</b> Gain stats equal to the Attack of the minions that
    # <b>Infused</b> this.
    pass


class REV_023:
    """Demolition Renovator"""

    # <b>Battlecry:</b> Destroy an enemy location.
    pass
