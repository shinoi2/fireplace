from ..utils import *

##
# Minions


class CS3_017:
    """Gan'arg Glaivesmith"""

    # <b>Outcast:</b> Give your hero +3_Attack this turn.
    outcast = Buff(FRIENDLY_HERO, "CS3_017e")


CS3_017e = buff(atk=3)


class CS3_019:
    """Kor'vas Bloodthorn"""

    # [x]<b>Charge</b>, <b>Lifesteal</b> After you play a card with
    # <b>Outcast</b>, return this to your hand.
    events = Play(CONTROLLER, OUTCAST).after(Bounce(SELF))


class CS3_020:
    """Illidari Inquisitor"""

    # <b>Rush</b>. After your hero attacks an enemy, this attacks it too.
    events = Attack(FRIENDLY_HERO, ENEMY_CHARACTERS).after(
        Dead(Attack.DEFENDER) | Attack(SELF, Attack.DEFENDER)
    )
