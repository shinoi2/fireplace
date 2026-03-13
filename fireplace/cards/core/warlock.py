from ..utils import *

##
# Minions


class CS3_003:
    """Felsoul Jailer"""

    # [x]<b>Battlecry:</b> Your opponent discards a minion. <b>Deathrattle:</b>
    # Return it.
    play = Discard(OPPONENT, RANDOM(ENEMY_HAND + MINION)).then(
        Find(Discard.TARGET) & Retarget(SELF, Discard.TARGET)
    )
    deathrattle = Give(OPPONENT, TARGET)


class CS3_021:
    """Enslaved Fel Lord"""

    # <b>Taunt</b>. Also damages the minions next to whomever this attacks.
    events = Attack(SELF).on(CLEAVE)


##
# Spells


class CS3_002:
    """Ritual of Doom"""

    # Destroy a friendly minion. If you had 5 or more, summon a 5/5 Demon.
    play = (
        Destroy(TARGET),
        (Count(FRIENDLY_MINIONS) >= 5) & Summon(CONTROLLER, "CS3_002t"),
    )
