from ..utils import *

##
# Minions


class SW_400:
    """Entrapped Sorceress"""

    # [x]<b>Battlecry:</b> If you control a _<b>Quest</b>, <b>Discover</b> a
    # spell.
    powered_up = Find(FRIENDLY_QUEST)
    play = powered_up & DISCOVER(RandomSpell())


class SW_306:
    """Encumbered Pack Mule"""

    # [x]<b>Taunt</b> When you draw this, add a _copy of it to your hand.
    draw = Give(CONTROLLER, ExactCopy(SELF))


class SW_036:
    """Two-Faced Investor"""

    # [x]At the end of your turn, reduce the Cost of a card in your hand by
    # (1). <i>(50% chance to increase.)</i>
    events = OWN_TURN_END.on(
        COINFLIP & Buff(RANDOM(FRIENDLY_HAND), "SW_036e")
        | Buff(RANDOM(FRIENDLY_HAND), "SW_036e2")
    )


class SW_036e:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


class SW_036e2:
    tags = {GameTag.COST: +1}
    events = REMOVED_IN_PLAY


class SW_062:
    """Goldshire Gnoll"""

    # [x]<b>Rush</b> Costs (1) less for each __other card in your hand.
    cost_mod = -Count(FRIENDLY_HAND - SELF)


class SW_070:
    """Mailbox Dancer"""

    # [x]<b>Battlecry:</b> Add a Coin to your hand. <b>Deathrattle:</b> Give
    # your opponent one.
    play = Give(CONTROLLER, THE_COIN)
    deathrattle = Give(OPPONENT, THE_COIN)


class DED_524:
    """Multicaster"""

    # [x]<b>Battlecry:</b> Draw a card for each different spell school _you've
    # cast this game.
    play = (
        Find(CARDS_PLAYED_THIS_GAME + ARCANE)
        & ForceDraw(RANDOM(FRIENDLY_DECK + ARCANE)),
        Find(CARDS_PLAYED_THIS_GAME + FIRE) & ForceDraw(RANDOM(FRIENDLY_DECK + FIRE)),
        Find(CARDS_PLAYED_THIS_GAME + FROST) & ForceDraw(RANDOM(FRIENDLY_DECK + FROST)),
        Find(CARDS_PLAYED_THIS_GAME + NATURE)
        & ForceDraw(RANDOM(FRIENDLY_DECK + NATURE)),
        Find(CARDS_PLAYED_THIS_GAME + HOLY) & ForceDraw(RANDOM(FRIENDLY_DECK + HOLY)),
        Find(CARDS_PLAYED_THIS_GAME + SHADOW)
        & ForceDraw(RANDOM(FRIENDLY_DECK + SHADOW)),
        Find(CARDS_PLAYED_THIS_GAME + FEL) & ForceDraw(RANDOM(FRIENDLY_DECK + FEL)),
    )
