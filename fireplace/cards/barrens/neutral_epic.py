from ..utils import *

##
# Minions


class BAR_042:
    """Primordial Protector"""

    # [x]<b>Battlecry:</b> Draw your highest Cost spell. Summon a random minion
    # with the same Cost.
    play = ForceDraw(RANDOM(HIGHEST_COST(FRIENDLY_DECK + SPELL))).then(
        Summon(RandomMinion(cost=COST(ForceDraw.TARGET)))
    )


class BAR_073:
    """Barrens Blacksmith"""

    # <b>Frenzy:</b> Give your other minions +2/+2.
    frenzy = Buff(FRIENDLY_MINIONS - SELF, "BAR_073e")


BAR_073e = buff(+2, +2)


class BAR_075:
    """Crossroads Watch Post"""

    # [x]Can't attack. Whenever your opponent casts a spell, give your minions
    # +1/+1.
    events = Play(OPPONENT, SPELL).after(Buff(FRIENDLY_MINIONS, "BAR_075e"))


BAR_075e = buff(+1, +1)


class BAR_081:
    """Southsea Scoundrel"""

    # <b>Battlecry:</b> <b>Discover</b> a card in your opponent's deck. They
    # draw theirs as well.
    play = Choice(CONTROLLER, RANDOM(DeDuplicate(ENEMY_DECK)) * 3).then(
        ForceDraw(OPPONENT, Choice.CARD),
        Give(CONTROLLER, Copy(Choice.CARD)),
    )


class BAR_744:
    """Spirit Healer"""

    # After you cast a Holy spell, give a random friendly minion +2 Health.
    events = Play(CONTROLLER, HOLY).after(Buff(RANDOM_FRIENDLY_MINION, "BAR_744e"))


BAR_744e = buff(health=2)
