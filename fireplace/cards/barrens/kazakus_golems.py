from ..utils import *


class BAR_079t10:
    """Wildvine"""

    # <b>Battlecry:</b> Give your other minions +1/+1.
    play = Buff(FRIENDLY_MINIONS - SELF, "BAR_079t10e")


BAR_079t10e = buff(+1, +1)


class BAR_079t10b:
    """Wildvine"""

    # <b>Battlecry:</b> Give your other minions +2/+2.
    play = Buff(FRIENDLY_MINIONS - SELF, "BAR_079t10be")


BAR_079t10be = buff(+2, +2)


class bar_079t10c:
    """Wildvine"""

    # <b>Battlecry:</b> Give your other minions +4/+4.
    play = Buff(FRIENDLY_MINIONS - SELF, "BAR_079t10ce")


BAR_079t10ce = buff(+4, +4)


class BAR_079t11:
    """Gromsblood"""

    # <b>Battlecry:</b> Summon a copy of this.
    play = Summon(CONTROLLER, ExactCopy(SELF))


class BAR_079t12:
    """Icecap"""

    # <b>Battlecry:</b> <b>Freeze</b> a random enemy minion.
    play = Freeze(RANDOM_ENEMY_MINION)


class BAR_079t12b:
    """Icecap"""

    # <b>Battlecry:</b> <b>Freeze</b> two random enemy minions.
    play = Freeze(RANDOM_ENEMY_MINION * 2)


class BAR_079t12c:
    """Icecap"""

    # <b>Battlecry:</b> <b>Freeze</b> all enemy minions.
    play = Freeze(ENEMY_MINIONS)


class BAR_079t13:
    """Firebloom"""

    # <b>Battlecry:</b> Deal 3 damage to a random enemy minion.
    play = Hit(RANDOM_ENEMY_MINION, 3)


class BAR_079t13b:
    """Firebloom"""

    # <b>Battlecry:</b> Deal 3 damage to two random enemy minions.
    play = Hit(RANDOM_ENEMY_MINION * 2, 3)


class BAR_079t13c:
    """Firebloom"""

    # <b>Battlecry:</b> Deal 3 damage to all enemy minions.
    play = Hit(ENEMY_MINIONS, 3)


class BAR_079t15:
    """Kingsblood"""

    # <b>Battlecry:</b> Draw a card.
    play = Draw(CONTROLLER)


class BAR_079t15b:
    """Kingsblood"""

    # <b>Battlecry:</b> Draw 2 cards.
    play = Draw(CONTROLLER) * 2


class BAR_079t15c:
    """Kingsblood"""

    # <b>Battlecry:</b> Draw 4 cards.
    play = Draw(CONTROLLER) * 4
