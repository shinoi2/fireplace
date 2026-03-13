from ..utils import *

##
# Spells


class CS3_016:
    """Reckoning"""

    # <b>Secret:</b> After an enemy minion deals 3 or more damage, destroy it.
    secret = Damage(source=ENEMY_MINIONS).after(
        (Damage.AMOUNT >= 3) & (Reveal(SELF), Destroy(SOURCE))
    )


class CS3_029:
    """Pursuit of Justice"""

    # Give +1 Attack to Silver Hand Recruits you summon this game.
    play = Buff(CONTROLLER, "CS3_029e")


class CS3_029e:
    update = Refresh(FRIENDLY + ID("CS2_101t"), buff="CS3_029e2")


CS3_029e2 = buff(atk=1)
