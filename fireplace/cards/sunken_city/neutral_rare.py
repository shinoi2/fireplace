from ..utils import *

##
# Minions


class TSC_826:
    """Crushclaw Enforcer"""

    # <b>Battlecry:</b> If you've cast a spell while holding this, draw a Naga.
    powered_up = Find(CARDS_PLAYED_WHEN_HOLDING + SPELL)
    play = powered_up & FORCE_DRAW(NAGA)


class TSC_827:
    """Vicious Slitherspear"""

    # [x]After you cast a spell, gain +1 Attack until your next turn.
    events = Play(CONTROLLER, SPELL).after(Buff(SELF, "TSC_827e"))


TSC_827e = buff(atk=1)


class TSC_645:
    """Mothership"""

    # <b>Rush</b> <b>Deathrattle:</b> Summon two random Mechs that cost (3) or
    # less.
    deathrattle = Summon(CONTROLLER, RandomMech(cost=[0, 1, 2, 3])) * 2


class TSC_960:
    """Twin-fin Fin Twin"""

    # <b>Rush</b>. <b>Battlecry:</b> Summon a copy of this.
    play = Summon(CONTROLLER, ExactCopy(SELF))


class TID_710:
    """Snapdragon"""

    # [x]<b>Battlecry:</b> Give all <b>Battlecry</b> minions in your deck
    # +1/+1.
    play = Buff(FRIENDLY_DECK + BATTLECRY, "TID_710e")


TID_710e = buff(+1, +1)


class TID_744:
    """Coilfang Constrictor"""

    # [x]<b>Battlecry:</b> Look at 3 cards in your opponent's hand and choose
    # one. It can't be played next turn.
    play = Choice(CONTROLLER, RANDOM(ENEMY_HAND, 3)).then(Buff(Choice.CARD, "TID_744e"))


class TID_744e:
    tags = {GameTag.CANT_PLAY: True}
    events = OWN_TURN_END.on(Destroy(SELF))
